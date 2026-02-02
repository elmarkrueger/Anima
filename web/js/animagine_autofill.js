import { app } from "../../../scripts/app.js";

// Character to Series/Artist mapping - loaded from CSV data
const CHARACTER_MAPPING = {
    "Son Goku": { series: "Dragon Ball", artist: "toriyama_akira" },
    "Monkey D. Luffy": { series: "One Piece", artist: "oda_eiichiro" },
    "Naruto Uzumaki": { series: "Naruto", artist: "kishimoto_masashi" },
    "Sailor Moon (Usagi Tsukino)": { series: "Sailor Moon", artist: "takeuchi_naoko" },
    "Levi Ackerman": { series: "Attack on Titan", artist: "isayama_hajime" },
    "Edward Elric": { series: "Fullmetal Alchemist", artist: "arakawa_hiromu" },
    "Guts": { series: "Berserk", artist: "miura_kentarou" },
    "Spike Spiegel": { series: "Cowboy Bebop", artist: "kawamoto_toshihiro" },
    "L Lawliet": { series: "Death Note", artist: "obata_takeshi" },
    "Satoru Gojo": { series: "Jujutsu Kaisen", artist: "akutami_gege" },
    "Saitama": { series: "One Punch Man", artist: "murata_yusuke" },
    "Jotaro Kujo": { series: "JoJo's Bizarre Adventure", artist: "araki_hirohiko" },
    "Rei Ayanami": { series: "Neon Genesis Evangelion", artist: "sadamoto_yoshiyuki" },
    "Tanjiro Kamado": { series: "Demon Slayer (Kimetsu no Yaiba)", artist: "gotouge_koyoharu" },
    "Lelouch Lamperouge": { series: "Code Geass", artist: "clamp" },
    "Pikachu": { series: "Pokemon", artist: "sugimori_ken" },
    "Killua Zoldyck": { series: "Hunter x Hunter", artist: "togashi_yoshihiro" },
    "Rem": { series: "Re:Zero - Starting Life in Another World", artist: "ootsuka_shinichirou" },
    "Makima": { series: "Chainsaw Man", artist: "fujimoto_tatsuki" },
    "Astro Boy": { series: "Astro Boy", artist: "tezuka_osamu" },
    "Yor Forger": { series: "Spy x Family", artist: "endou_tatsuya" },
    "Sakata Gintoki": { series: "Gintama", artist: "sorachi_hideaki" },
    "Totoro": { series: "My Neighbor Totoro", artist: "miyazaki_hayao" },
    "Motoko Kusanagi": { series: "Ghost in the Shell", artist: "shirow_masamune" },
    "Roronoa Zoro": { series: "One Piece", artist: "oda_eiichiro" },
    "Vegeta": { series: "Dragon Ball", artist: "toriyama_akira" },
    "Sakura Kinomoto": { series: "Cardcaptor Sakura", artist: "clamp" },
    "Eren Yeager": { series: "Attack on Titan", artist: "isayama_hajime" },
    "Violet Evergarden": { series: "Violet Evergarden", artist: "takase_akiko" },
    "Frieren": { series: "Frieren: Beyond Journey's End", artist: "abe_tsukasa" },
};

app.registerExtension({
    name: "Animagine.CharacterAutofill",
    
    async nodeCreated(node) {
        // Only apply to Character Factory node
        if (node.comfyClass !== "AnimagineXL4_Character_Factory") {
            return;
        }
        
        // Find the widgets we need
        const characterWidget = node.widgets?.find(w => w.name === "character_name");
        const seriesWidget = node.widgets?.find(w => w.name === "series_name");
        const artistWidget = node.widgets?.find(w => w.name === "artist_tag");
        
        if (!characterWidget || !seriesWidget || !artistWidget) {
            return;
        }
        
        // Store original callback if exists
        const originalCallback = characterWidget.callback;
        
        // Override the callback for character_name widget
        characterWidget.callback = function(value, graphCanvas, node, pos, event) {
            // Call original callback if it exists
            if (originalCallback) {
                originalCallback.call(this, value, graphCanvas, node, pos, event);
            }
            
            // Auto-fill series and artist based on character selection
            if (value && value !== "None" && CHARACTER_MAPPING[value]) {
                const mapping = CHARACTER_MAPPING[value];
                
                // Update series_name if it's currently "None" or matches another character's series
                if (seriesWidget.value === "None" || shouldAutoUpdate(seriesWidget, mapping.series)) {
                    seriesWidget.value = mapping.series;
                }
                
                // Update artist_tag if it's currently "None" or matches another character's artist
                if (artistWidget.value === "None" || shouldAutoUpdate(artistWidget, mapping.artist)) {
                    artistWidget.value = mapping.artist;
                }
                
                // Trigger node update
                node.setDirtyCanvas(true, true);
            }
        };
    }
});

// Helper function to determine if we should auto-update a widget
function shouldAutoUpdate(widget, newValue) {
    const currentValue = widget.value;
    
    // Always update if current is "None"
    if (currentValue === "None") {
        return true;
    }
    
    // Check if current value belongs to any character mapping
    // If so, it was likely auto-filled, so we can update it
    for (const charData of Object.values(CHARACTER_MAPPING)) {
        if (currentValue === charData.series || currentValue === charData.artist) {
            return true;
        }
    }
    
    return false;
}
