using System;
using System.Collections.Generic;
using System.Text;

namespace BlackjackGUI
{
    public class JoinResponse
    {
        public string player_id { get; set; } = "";
        public bool is_host { get; set; }
        public string message { get; set; } = "";
    }
}
