namespace BlackjackGUI
{
    public class GameStateResponse
    {
        public string game_state { get; set; } = "";
        public string message { get; set; } = "";

        public List<PlayerInfo> players { get; set; } = new();

        public List<string> valid_choices { get; set; } = new();

        public int current_hand_index { get; set; }

        public List<string> players_missing_actions { get; set; } = new();

        public HandInfo? dealer_hand { get; set; }

        public List<System.Text.Json.JsonElement> bet_settlements { get; set; } = new();
    }

    public class PlayerInfo
    {
        public string player_id { get; set; } = "";
        public string name { get; set; } = "";
        public int balance { get; set; }

        public List<HandInfo> hands { get; set; } = new();
    }

    public class HandInfo
    {
        public List<CardInfo> cards { get; set; } = new();
        public int value { get; set; }
        public decimal? bet { get; set; }
        public bool bust { get; set; }
        public bool blackjack { get; set; }
        public bool stand { get; set; }
    }

    public class CardInfo
    {
        public string suit { get; set; } = "";
        public string rank { get; set; } = "";
    }
}