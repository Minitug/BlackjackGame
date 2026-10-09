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

        private string playerId = "";
        private bool isHost = false;
        private bool hasPlacedBet = false;
        private int currentBet = 0;

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
    }
}
