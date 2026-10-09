using System;
using System.Collections.Generic;
using System.Text;

namespace BlackjackGUI
{
    public class GameStateResponse
    {
        public string game_state { get; set; } = "";
        public List<PlayerInfo> players { get; set; } = new();
        public string message { get; set; } = "";
    }

    public class PlayerInfo
    {
        public string player_id { get; set; } = "";
        public string name { get; set; } = "";
        public int balance { get; set; }
    }

}