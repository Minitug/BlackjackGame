namespace BlackjackGUI
{
    partial class BlackjackForm
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            lblTitle = new Label();
            lblNamePrompt = new Label();
            txtPlayerName = new TextBox();
            btnJoin = new Button();
            pnlLobby = new Panel();
            btnRefresh = new Button();
            btnStart = new Button();
            lblLobbyStatus = new Label();
            lstPlayers = new ListBox();
            lblLobbyTitle = new Label();
            pnlJoin = new Panel();
            pnlGame = new Panel();
            btnPlaceBet = new Button();
            btnGameRefresh = new Button();
            btnSplit = new Button();
            btnSurrender = new Button();
            btnDouble = new Button();
            btnStand = new Button();
            btnHit = new Button();
            txtBetAmount = new TextBox();
            lblGameMessage = new Label();
            lblBetAmount = new Label();
            lblBet = new Label();
            lblBalance = new Label();
            lblPlayerHand = new Label();
            lblDealerHand = new Label();
            lblGameState = new Label();
            txtRoundResults = new TextBox();
            pnlLobby.SuspendLayout();
            pnlJoin.SuspendLayout();
            pnlGame.SuspendLayout();
            SuspendLayout();
            // 
            // lblTitle
            // 
            lblTitle.AutoSize = true;
            lblTitle.Font = new Font("Segoe UI", 72F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblTitle.ForeColor = SystemColors.ControlText;
            lblTitle.Location = new Point(855, 40);
            lblTitle.Name = "lblTitle";
            lblTitle.Size = new Size(657, 191);
            lblTitle.TabIndex = 0;
            lblTitle.Text = "Blackjack";
            // 
            // lblNamePrompt
            // 
            lblNamePrompt.AutoSize = true;
            lblNamePrompt.Font = new Font("Segoe UI", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblNamePrompt.Location = new Point(1022, 255);
            lblNamePrompt.Name = "lblNamePrompt";
            lblNamePrompt.Size = new Size(303, 48);
            lblNamePrompt.TabIndex = 1;
            lblNamePrompt.Text = "Choose username";
            // 
            // txtPlayerName
            // 
            txtPlayerName.Font = new Font("Segoe UI", 16F, FontStyle.Regular, GraphicsUnit.Point, 0);
            txtPlayerName.Location = new Point(489, 327);
            txtPlayerName.Name = "txtPlayerName";
            txtPlayerName.Size = new Size(1425, 50);
            txtPlayerName.TabIndex = 2;
            txtPlayerName.Text = "Enter your name...";
            // 
            // btnJoin
            // 
            btnJoin.BackColor = SystemColors.Highlight;
            btnJoin.Font = new Font("Segoe UI", 16F, FontStyle.Regular, GraphicsUnit.Point, 0);
            btnJoin.ForeColor = SystemColors.Control;
            btnJoin.Location = new Point(1022, 398);
            btnJoin.Name = "btnJoin";
            btnJoin.Size = new Size(292, 79);
            btnJoin.TabIndex = 3;
            btnJoin.Text = "Join Game";
            btnJoin.UseVisualStyleBackColor = false;
            btnJoin.Click += btnJoin_Click;
            // 
            // pnlLobby
            // 
            pnlLobby.Controls.Add(btnRefresh);
            pnlLobby.Controls.Add(btnStart);
            pnlLobby.Controls.Add(lblLobbyStatus);
            pnlLobby.Controls.Add(lstPlayers);
            pnlLobby.Controls.Add(lblLobbyTitle);
            pnlLobby.Dock = DockStyle.Fill;
            pnlLobby.Location = new Point(0, 0);
            pnlLobby.Name = "pnlLobby";
            pnlLobby.Size = new Size(2466, 1141);
            pnlLobby.TabIndex = 4;
            // 
            // btnRefresh
            // 
            btnRefresh.BackColor = SystemColors.AppWorkspace;
            btnRefresh.Font = new Font("Segoe UI", 16F, FontStyle.Regular, GraphicsUnit.Point, 0);
            btnRefresh.ForeColor = SystemColors.Control;
            btnRefresh.Location = new Point(432, 247);
            btnRefresh.Name = "btnRefresh";
            btnRefresh.Size = new Size(379, 86);
            btnRefresh.TabIndex = 4;
            btnRefresh.Text = "Refresh";
            btnRefresh.UseVisualStyleBackColor = false;
            btnRefresh.Click += btnRefresh_Click;
            // 
            // btnStart
            // 
            btnStart.BackColor = SystemColors.Highlight;
            btnStart.Font = new Font("Segoe UI", 16F, FontStyle.Regular, GraphicsUnit.Point, 0);
            btnStart.ForeColor = SystemColors.Control;
            btnStart.Location = new Point(47, 247);
            btnStart.Name = "btnStart";
            btnStart.Size = new Size(379, 86);
            btnStart.TabIndex = 3;
            btnStart.Text = "Start Game";
            btnStart.UseVisualStyleBackColor = false;
            btnStart.Click += btnStart_Click;
            // 
            // lblLobbyStatus
            // 
            lblLobbyStatus.AutoSize = true;
            lblLobbyStatus.Font = new Font("Segoe UI", 14F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblLobbyStatus.Location = new Point(47, 206);
            lblLobbyStatus.Name = "lblLobbyStatus";
            lblLobbyStatus.Size = new Size(328, 38);
            lblLobbyStatus.TabIndex = 2;
            lblLobbyStatus.Text = "Waiting for host to start...";
            // 
            // lstPlayers
            // 
            lstPlayers.Font = new Font("Segoe UI", 14F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lstPlayers.FormattingEnabled = true;
            lstPlayers.Location = new Point(47, 83);
            lstPlayers.Name = "lstPlayers";
            lstPlayers.Size = new Size(764, 118);
            lstPlayers.TabIndex = 1;
            // 
            // lblLobbyTitle
            // 
            lblLobbyTitle.AutoSize = true;
            lblLobbyTitle.Font = new Font("Segoe UI", 18F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblLobbyTitle.Location = new Point(36, 28);
            lblLobbyTitle.Name = "lblLobbyTitle";
            lblLobbyTitle.Size = new Size(212, 48);
            lblLobbyTitle.TabIndex = 0;
            lblLobbyTitle.Text = "Game lobby";
            // 
            // pnlJoin
            // 
            pnlJoin.BackColor = SystemColors.ControlDarkDark;
            pnlJoin.Controls.Add(btnJoin);
            pnlJoin.Controls.Add(txtPlayerName);
            pnlJoin.Controls.Add(lblNamePrompt);
            pnlJoin.Controls.Add(lblTitle);
            pnlJoin.Dock = DockStyle.Fill;
            pnlJoin.Location = new Point(0, 0);
            pnlJoin.Name = "pnlJoin";
            pnlJoin.Size = new Size(2466, 1141);
            pnlJoin.TabIndex = 5;
            pnlJoin.Visible = false;
            // 
            // pnlGame
            // 
            pnlGame.BackColor = Color.DarkGreen;
            pnlGame.Controls.Add(txtRoundResults);
            pnlGame.Controls.Add(btnPlaceBet);
            pnlGame.Controls.Add(btnGameRefresh);
            pnlGame.Controls.Add(btnSplit);
            pnlGame.Controls.Add(btnSurrender);
            pnlGame.Controls.Add(btnDouble);
            pnlGame.Controls.Add(btnStand);
            pnlGame.Controls.Add(btnHit);
            pnlGame.Controls.Add(txtBetAmount);
            pnlGame.Controls.Add(lblGameMessage);
            pnlGame.Controls.Add(lblBetAmount);
            pnlGame.Controls.Add(lblBet);
            pnlGame.Controls.Add(lblBalance);
            pnlGame.Controls.Add(lblPlayerHand);
            pnlGame.Controls.Add(lblDealerHand);
            pnlGame.Controls.Add(lblGameState);
            pnlGame.Dock = DockStyle.Fill;
            pnlGame.Location = new Point(0, 0);
            pnlGame.Name = "pnlGame";
            pnlGame.Size = new Size(2466, 1141);
            pnlGame.TabIndex = 5;
            // 
            // btnPlaceBet
            // 
            btnPlaceBet.BackColor = Color.YellowGreen;
            btnPlaceBet.Location = new Point(795, 911);
            btnPlaceBet.Name = "btnPlaceBet";
            btnPlaceBet.Size = new Size(170, 34);
            btnPlaceBet.TabIndex = 14;
            btnPlaceBet.Text = "Place bet";
            btnPlaceBet.UseVisualStyleBackColor = false;
            btnPlaceBet.Click += btnPlaceBet_Click;
            // 
            // btnGameRefresh
            // 
            btnGameRefresh.BackColor = Color.YellowGreen;
            btnGameRefresh.Location = new Point(2284, 1038);
            btnGameRefresh.Name = "btnGameRefresh";
            btnGameRefresh.Size = new Size(170, 91);
            btnGameRefresh.TabIndex = 13;
            btnGameRefresh.Text = "Refresh";
            btnGameRefresh.UseVisualStyleBackColor = false;
            // 
            // btnSplit
            // 
            btnSplit.BackColor = Color.YellowGreen;
            btnSplit.Location = new Point(786, 971);
            btnSplit.Name = "btnSplit";
            btnSplit.Size = new Size(170, 91);
            btnSplit.TabIndex = 12;
            btnSplit.Text = "Split";
            btnSplit.UseVisualStyleBackColor = false;
            btnSplit.Click += btnSplit_Click;
            // 
            // btnSurrender
            // 
            btnSurrender.BackColor = Color.YellowGreen;
            btnSurrender.Location = new Point(595, 971);
            btnSurrender.Name = "btnSurrender";
            btnSurrender.Size = new Size(170, 91);
            btnSurrender.TabIndex = 11;
            btnSurrender.Text = "Surrender";
            btnSurrender.UseVisualStyleBackColor = false;
            btnSurrender.Click += btnSurrender_Click;
            // 
            // btnDouble
            // 
            btnDouble.BackColor = Color.YellowGreen;
            btnDouble.Location = new Point(400, 971);
            btnDouble.Name = "btnDouble";
            btnDouble.Size = new Size(170, 91);
            btnDouble.TabIndex = 10;
            btnDouble.Text = "Double down";
            btnDouble.UseVisualStyleBackColor = false;
            btnDouble.Click += btnDouble_Click;
            // 
            // btnStand
            // 
            btnStand.BackColor = Color.YellowGreen;
            btnStand.Location = new Point(205, 971);
            btnStand.Name = "btnStand";
            btnStand.Size = new Size(170, 91);
            btnStand.TabIndex = 9;
            btnStand.Text = "Stand";
            btnStand.UseVisualStyleBackColor = false;
            btnStand.Click += btnStand_Click;
            // 
            // btnHit
            // 
            btnHit.BackColor = Color.YellowGreen;
            btnHit.Location = new Point(12, 971);
            btnHit.Name = "btnHit";
            btnHit.Size = new Size(170, 91);
            btnHit.TabIndex = 8;
            btnHit.Text = "Hit";
            btnHit.UseVisualStyleBackColor = false;
            btnHit.Click += btnHit_Click;
            // 
            // txtBetAmount
            // 
            txtBetAmount.Location = new Point(179, 914);
            txtBetAmount.Name = "txtBetAmount";
            txtBetAmount.Size = new Size(586, 31);
            txtBetAmount.TabIndex = 7;
            // 
            // lblGameMessage
            // 
            lblGameMessage.AutoSize = true;
            lblGameMessage.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblGameMessage.ForeColor = SystemColors.Control;
            lblGameMessage.Location = new Point(12, 1076);
            lblGameMessage.Name = "lblGameMessage";
            lblGameMessage.Size = new Size(430, 32);
            lblGameMessage.TabIndex = 6;
            lblGameMessage.Text = "Server messages will be displayed here";
            // 
            // lblBetAmount
            // 
            lblBetAmount.AutoSize = true;
            lblBetAmount.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblBetAmount.ForeColor = SystemColors.Control;
            lblBetAmount.Location = new Point(12, 911);
            lblBetAmount.Name = "lblBetAmount";
            lblBetAmount.Size = new Size(139, 32);
            lblBetAmount.TabIndex = 5;
            lblBetAmount.Text = "Bet amount";
            // 
            // lblBet
            // 
            lblBet.AutoSize = true;
            lblBet.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblBet.ForeColor = SystemColors.Control;
            lblBet.Location = new Point(2256, 818);
            lblBet.Name = "lblBet";
            lblBet.Size = new Size(49, 32);
            lblBet.TabIndex = 4;
            lblBet.Text = "Bet";
            // 
            // lblBalance
            // 
            lblBalance.AutoSize = true;
            lblBalance.Font = new Font("Segoe UI", 12F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblBalance.ForeColor = SystemColors.Control;
            lblBalance.Location = new Point(12, 818);
            lblBalance.Name = "lblBalance";
            lblBalance.Size = new Size(96, 32);
            lblBalance.TabIndex = 3;
            lblBalance.Text = "Balance";
            // 
            // lblPlayerHand
            // 
            lblPlayerHand.AutoSize = true;
            lblPlayerHand.Font = new Font("Segoe UI", 16F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblPlayerHand.ForeColor = SystemColors.Control;
            lblPlayerHand.Location = new Point(1022, 445);
            lblPlayerHand.Name = "lblPlayerHand";
            lblPlayerHand.Size = new Size(211, 45);
            lblPlayerHand.TabIndex = 2;
            lblPlayerHand.Text = "Player's Hand";
            // 
            // lblDealerHand
            // 
            lblDealerHand.AutoSize = true;
            lblDealerHand.Font = new Font("Segoe UI", 16F, FontStyle.Regular, GraphicsUnit.Point, 0);
            lblDealerHand.ForeColor = SystemColors.Control;
            lblDealerHand.Location = new Point(1020, 70);
            lblDealerHand.Name = "lblDealerHand";
            lblDealerHand.Size = new Size(217, 45);
            lblDealerHand.TabIndex = 1;
            lblDealerHand.Text = "Dealer's Hand";
            // 
            // lblGameState
            // 
            lblGameState.AutoSize = true;
            lblGameState.ForeColor = SystemColors.Control;
            lblGameState.Location = new Point(2256, 15);
            lblGameState.Name = "lblGameState";
            lblGameState.Size = new Size(97, 25);
            lblGameState.TabIndex = 0;
            lblGameState.Text = "GameState";
            // 
            // txtRoundResults
            // 
            txtRoundResults.BackColor = Color.DarkGreen;
            txtRoundResults.ForeColor = SystemColors.Control;
            txtRoundResults.Location = new Point(1642, 772);
            txtRoundResults.Multiline = true;
            txtRoundResults.Name = "txtRoundResults";
            txtRoundResults.ReadOnly = true;
            txtRoundResults.ScrollBars = ScrollBars.Both;
            txtRoundResults.Size = new Size(555, 357);
            txtRoundResults.TabIndex = 15;
            txtRoundResults.Visible = false;
            // 
            // BlackjackForm
            // 
            AutoScaleDimensions = new SizeF(10F, 25F);
            AutoScaleMode = AutoScaleMode.Font;
            BackColor = SystemColors.ActiveBorder;
            ClientSize = new Size(2466, 1141);
            Controls.Add(pnlGame);
            Controls.Add(pnlLobby);
            Controls.Add(pnlJoin);
            Name = "BlackjackForm";
            Text = "BlackjackForm";
            pnlLobby.ResumeLayout(false);
            pnlLobby.PerformLayout();
            pnlJoin.ResumeLayout(false);
            pnlJoin.PerformLayout();
            pnlGame.ResumeLayout(false);
            pnlGame.PerformLayout();
            ResumeLayout(false);
        }

        #endregion

        private Label lblTitle;
        private Label lblNamePrompt;
        private TextBox txtPlayerName;
        private Button btnJoin;
        private Panel pnlLobby;
        private Button btnRefresh;
        private Button btnStart;
        private Label lblLobbyStatus;
        private ListBox lstPlayers;
        private Label lblLobbyTitle;
        private Panel pnlJoin;
        private Panel pnlGame;
        private Label lblDealerHand;
        private Label lblGameState;
        private Label lblGameMessage;
        private Label lblBetAmount;
        private Label lblBet;
        private Label lblBalance;
        private Label lblPlayerHand;
        private Button btnPlaceBet;
        private Button btnGameRefresh;
        private Button btnSplit;
        private Button btnSurrender;
        private Button btnDouble;
        private Button btnStand;
        private Button btnHit;
        private TextBox txtBetAmount;
        private TextBox txtRoundResults;
    }
}
