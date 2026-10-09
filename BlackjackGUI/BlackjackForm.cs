using System.Net.Http.Json;
using static System.Runtime.InteropServices.JavaScript.JSType;
//using System.Xml.Linq;

namespace BlackjackGUI
{

    public partial class BlackjackForm : Form
    {
        public BlackjackForm()
        {
            InitializeComponent();

            Button[] actionButtons =
            {
                btnHit,
                btnStand,
                btnDouble,
                btnSplit,
                btnSurrender
            };

            foreach (Button button in actionButtons)
            {
                button.UseVisualStyleBackColor = false;
                actionButtonColors[button] = button.BackColor;
            }

            ShowJoinScreen();

            gameTimer.Tick += GameTimer_Tick;
        }

        private readonly HttpClient http = new HttpClient
        {
            BaseAddress = new Uri("http://127.0.0.1:8000")
        };

        private readonly System.Windows.Forms.Timer gameTimer = new()
        {
            Interval = 1000
        };

        private readonly Dictionary<Button, Color> actionButtonColors = new();

        private readonly Color disabledButtonColor = Color.LightGray;

        private string playerId = "";
        private bool isHost = false;
        private bool hasPlacedBet = false;
        private int currentBet = 0;
        private bool actionInProgress = false;
        private string previousGameState = "";


        private void ShowJoinScreen()
        {
            pnlJoin.Visible = true;
            pnlLobby.Visible = false;
            pnlGame.Visible = false;
            pnlJoin.BringToFront();
        }

        private void ShowLobbyScreen()
        {
            pnlJoin.Visible = false;
            pnlLobby.Visible = true;
            pnlGame.Visible = false;
            pnlLobby.BringToFront();
        }

        private void ShowGameScreen()
        {
            pnlJoin.Visible = false;
            pnlLobby.Visible = false;
            pnlGame.Visible = true;
            pnlGame.BringToFront();
        }

        private async Task RefreshLobbyAsync()
        {
            try
            {
                var state = await http.GetFromJsonAsync<GameStateResponse>(
                    "/game/state"
                );

                if (state == null)
                    return;

                lstPlayers.Items.Clear();

                foreach (var player in state.players)
                {
                    lstPlayers.Items.Add(player.name);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Could not refresh lobby: {ex.Message}");
            }
        }

        private async void btnJoin_Click(object sender, EventArgs e)
        {
            string name = txtPlayerName.Text.Trim();

            if (string.IsNullOrWhiteSpace(name))
            {
                MessageBox.Show("Please enter your name.");
                return;
            }

            try
            {
                var response = await http.PostAsJsonAsync(
                    "/player/add",
                    new { name = name }
                );

                response.EnsureSuccessStatusCode();

                var data = await response.Content.ReadFromJsonAsync<JoinResponse>();

                if (data == null)
                    return;

                playerId = data.player_id;
                isHost = data.is_host;

                btnStart.Enabled = isHost;

                if (isHost)
                {
                    lblLobbyStatus.Text = "Waiting for players. Press Start to begin.";
                }
                else
                {
                    lblLobbyStatus.Text = "Waiting for host to start...";
                }

                ShowLobbyScreen();

                await RefreshLobbyAsync();

                gameTimer.Start();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Could not connect to server: {ex.Message}");
            }
        }

        private async void btnRefresh_Click(object sender, EventArgs e)
        {
            await RefreshLobbyAsync();
        }

        private async void btnStart_Click(object sender, EventArgs e)
        {
            if (!isHost)
                return;
            
            try
            {
                var response = await http.PostAsJsonAsync(
                "/game/start",
                new { player_id = playerId }
                );

                response.EnsureSuccessStatusCode();

                //MessageBox.Show("Game started successfully");
            }

            catch (Exception ex)
            {
                MessageBox.Show($"Could not start game: {ex.Message}");
            }
        }

        private async Task RefreshGameStateAsync()
        {
            var state = await http.GetFromJsonAsync<GameStateResponse>(
                "/game/state"
            );

            if (state == null)
                return;

            var currentPlayer = state.players.Find(
                p => p.player_id == playerId
            );

            if (currentPlayer != null)
            {
                lblBalance.Text = $"Balance: {currentPlayer.balance}";
            }

            if (state.game_state == "Lobby")
            {
                if (!pnlLobby.Visible)
                    ShowLobbyScreen();

                lstPlayers.Items.Clear();

                foreach (var player in state.players)
                {
                    lstPlayers.Items.Add(player.name);
                }
            }
            else
            {
                if (!pnlGame.Visible)
                    ShowGameScreen();

                lblGameState.Text = state.game_state;
                lblGameMessage.Text = state.message;
            }

            if (state.game_state == "Round End" &&
                previousGameState != "Round End")
            {
                ShowRoundResults(state);
            }

            previousGameState = state.game_state;

            //var currentPlayer = state.players.Find(
            //    p => p.player_id == playerId
            //);

            if (currentPlayer != null && currentPlayer.hands.Count > 0)
            {
                int handIndex = state.current_hand_index;

                if (handIndex >= 0 && handIndex < currentPlayer.hands.Count)
                {
                    var hand = currentPlayer.hands[handIndex];

                    string cards = string.Join(", ",
                        hand.cards.Select(card => $"{card.rank} of {card.suit}")
                    );

                    lblPlayerHand.Text = $"Your hand: {cards} (Value: {hand.value})";

                    lblBet.Text = $"Bet: {hand.bet}";
                }
            }

            bool isPlaying = state.game_state == "Playing";

            bool isMyTurn =
                !actionInProgress &&
                state.players_missing_actions.Contains(playerId);

            bool canAct =
                state.game_state == "Playing" &&
                !actionInProgress &&
                state.players_missing_actions.Contains(playerId);

            SetActionButtonState(
                btnHit,
                canAct && state.valid_choices.Contains("H")
            );

            SetActionButtonState(
                btnStand,
                canAct && state.valid_choices.Contains("S")
            );

            SetActionButtonState(
                btnDouble,
                canAct && state.valid_choices.Contains("D")
            );

            SetActionButtonState(
                btnSplit,
                canAct && state.valid_choices.Contains("P")
            );

            SetActionButtonState(
                btnSurrender,
                canAct && state.valid_choices.Contains("R")
            );
        }

        private async void GameTimer_Tick(object? sender, EventArgs e)
        {
            gameTimer.Stop();

            try
            {
                await RefreshGameStateAsync();
            }
            catch (Exception ex)
            {
                System.Diagnostics.Debug.WriteLine(ex.Message);
            }
            finally
            {
                if (!IsDisposed)
                    gameTimer.Start();
            }
        }

        private async void btnPlaceBet_Click(object sender, EventArgs e)
        {
            if (!int.TryParse(txtBetAmount.Text, out int betAmount))
            {
                MessageBox.Show("Please enter a valid number.");
                return;
            }

            if (betAmount < 0)
            {
                MessageBox.Show("Bet cannot be negative.");
                return;
            }

            try
            {
                btnPlaceBet.Enabled = false;

                var response = await http.PostAsJsonAsync(
                    "/player/bet",
                    new
                    {
                        player_id = playerId,
                        bet_value = betAmount
                    }
                );

                response.EnsureSuccessStatusCode();

                hasPlacedBet = true;

                currentBet = betAmount;
                lblBet.Text = $"Bet: {betAmount}";

                await RefreshGameStateAsync();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Could not place bet: {ex.Message}");
                btnPlaceBet.Enabled = true;
            }
        }

        //private async Task SendPlayerActionAsync(string action)
        //{
        //    try
        //    {
        //        // Prevent repeated clicks while the request is being sent
        //        SetActionButtonsEnabled(false);

        //        var response = await http.PostAsJsonAsync(
        //            "/player/action",
        //            new
        //            {
        //                player_id = playerId,
        //                action = action
        //            }
        //        );

        //        response.EnsureSuccessStatusCode();

        //        // Immediately fetch the updated cards and game state
        //        await RefreshGameStateAsync();
        //    }
        //    catch (Exception ex)
        //    {
        //        MessageBox.Show($"Could not perform action: {ex.Message}");
        //    }
        //}

        private void SetActionButtonsEnabled(bool enabled)
        {
            SetActionButtonState(btnHit, enabled);
            SetActionButtonState(btnStand, enabled);
            SetActionButtonState(btnDouble, enabled);
            SetActionButtonState(btnSplit, enabled);
            SetActionButtonState(btnSurrender, enabled);
        }

        private async void btnHit_Click(object sender, EventArgs e)
        {
            await SendPlayerActionAsync("H");
        }

        private async void btnStand_Click(object sender, EventArgs e)
        {
            await SendPlayerActionAsync("S");
        }

        private async void btnDouble_Click(object sender, EventArgs e)
        {
            await SendPlayerActionAsync("D");
        }

        private async void btnSplit_Click(object sender, EventArgs e)
        {
            await SendPlayerActionAsync("P");
        }

        private async void btnSurrender_Click(object sender, EventArgs e)
        {
            await SendPlayerActionAsync("R");
        }

        private async Task SendPlayerActionAsync(string action)
        {
            if (actionInProgress)
                return;

            actionInProgress = true;
            SetActionButtonsEnabled(false);

            try
            {
                var response = await http.PostAsJsonAsync(
                    "/player/action",
                    new
                    {
                        player_id = playerId,
                        action = action
                    }
                );

                response.EnsureSuccessStatusCode();

                await RefreshGameStateAsync();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Could not perform action: {ex.Message}");
            }
            finally
            {
                actionInProgress = false;
                SetActionButtonsEnabled(false);
            }
        }

        private void SetActionButtonState(Button button, bool enabled)
        {
            button.Enabled = enabled;

            button.BackColor = enabled
                ? actionButtonColors[button]
                : disabledButtonColor;
        }

        private void ShowRoundResults(GameStateResponse state)
        {
            var results = new System.Text.StringBuilder();

            results.AppendLine("========== ROUND RESULTS ==========");
            results.AppendLine();

            foreach (var player in state.players)
            {
                results.AppendLine($"{player.name}'s hand:");

                foreach (var hand in player.hands)
                {
                    string cards = string.Join(", ",
                        hand.cards.Select(card =>
                            $"{card.rank} of {card.suit}")
                    );

                    results.AppendLine($"  {cards}");
                    results.AppendLine($"  Value: {hand.value}");
                }

                results.AppendLine();
            }

            results.AppendLine("Dealer's hand:");

            if (state.dealer_hand != null)
            {
                string dealerCards = string.Join(", ",
                    state.dealer_hand.cards.Select(card =>
                        $"{card.rank} of {card.suit}")
                );

                results.AppendLine($"  {dealerCards}");
                results.AppendLine($"  Value: {state.dealer_hand.value}");
            }

            results.AppendLine();
            results.AppendLine("------------- RESULTS -------------");
            results.AppendLine();

            foreach (var settlement in state.bet_settlements)
            {
                results.AppendLine(settlement.ToString());
            }

            txtRoundResults.Text = results.ToString();
            txtRoundResults.Visible = true;
        }
    }
}
