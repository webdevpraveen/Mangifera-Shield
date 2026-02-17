/**
 * 🛡️ Mangifera Shield — Voice Command Module
 * Web Speech API for Hinglish voice navigation
 */

let recognition = null;
let isListening = false;

// Voice command mapping (Hinglish)
const VOICE_COMMANDS = {
    // Navigation commands
    'home': 'dashboard', 'ghar': 'dashboard', 'dashboard': 'dashboard', 'डैशबोर्ड': 'dashboard',
    'scan': 'scanner', 'scanner': 'scanner', 'jaanch': 'scanner', 'jankari': 'scanner',
    'bimari': 'scanner', 'disease': 'scanner', 'बीमारी': 'scanner', 'जाँच': 'scanner',
    'photo': 'scanner', 'camera': 'scanner', 'kheencho': 'scanner',
    'khata': 'ledger', 'ledger': 'ledger', 'stock': 'ledger', 'स्टॉक': 'ledger',
    'khet khata': 'ledger', 'inventory': 'ledger', 'खाता': 'ledger',
    'mandi': 'mandi', 'rate': 'mandi', 'price': 'mandi', 'bhav': 'mandi',
    'daam': 'mandi', 'मंडी': 'mandi', 'भाव': 'mandi', 'रेट': 'mandi',
    'mausam': 'weather', 'weather': 'weather', 'alert': 'weather',
    'मौसम': 'weather', 'अलर्ट': 'weather', 'barish': 'weather',
    'certificate': 'certificate', 'pramanpatra': 'certificate', 'प्रमाणपत्र': 'certificate',
    'quality': 'certificate'
};

function initVoice() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
        console.log('⚠️ Web Speech API not supported');
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.maxAlternatives = 3;

    // Try Hindi first, fallback to English
    recognition.lang = 'hi-IN';

    recognition.onresult = handleVoiceResult;
    recognition.onerror = handleVoiceError;
    recognition.onend = handleVoiceEnd;

    // Setup toggle
    document.getElementById('voice-toggle').addEventListener('click', toggleVoice);
    document.getElementById('voice-close').addEventListener('click', stopVoice);
}

function toggleVoice() {
    if (isListening) {
        stopVoice();
    } else {
        startVoice();
    }
}

function startVoice() {
    if (!recognition) {
        initVoice();
        if (!recognition) {
            showToast('❌ Voice not supported in this browser');
            return;
        }
    }

    isListening = true;
    document.getElementById('voice-overlay').classList.remove('hidden');
    document.getElementById('voice-toggle').classList.add('active');
    document.getElementById('voice-transcript').textContent = '';
    document.getElementById('voice-status').textContent = t('voice_listening');

    try {
        recognition.start();
    } catch (e) {
        // Already started
        recognition.stop();
        setTimeout(() => recognition.start(), 100);
    }

    // Auto-stop after 10 seconds
    setTimeout(() => {
        if (isListening) stopVoice();
    }, 10000);
}

function stopVoice() {
    isListening = false;
    document.getElementById('voice-overlay').classList.add('hidden');
    document.getElementById('voice-toggle').classList.remove('active');

    if (recognition) {
        try { recognition.stop(); } catch (e) { }
    }
}

function handleVoiceResult(event) {
    let transcript = '';
    let isFinal = false;

    for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript = event.results[i][0].transcript.trim().toLowerCase();
        isFinal = event.results[i].isFinal;
    }

    document.getElementById('voice-transcript').textContent = transcript;

    if (isFinal) {
        processVoiceCommand(transcript);
    }
}

function processVoiceCommand(transcript) {
    console.log('🎤 Voice:', transcript);

    // Check each word in the transcript against commands
    const words = transcript.toLowerCase().split(/\s+/);

    for (const word of words) {
        if (VOICE_COMMANDS[word]) {
            const page = VOICE_COMMANDS[word];
            stopVoice();
            navigateTo(page);

            // Speak confirmation
            speak(currentLang === 'hi'
                ? `${getPageNameHi(page)} खोल रहे हैं`
                : `Opening ${page}`
            );

            showToast(`🎤 → ${page}`);
            return;
        }
    }

    // Check multi-word phrases
    for (const [phrase, page] of Object.entries(VOICE_COMMANDS)) {
        if (transcript.includes(phrase)) {
            stopVoice();
            navigateTo(page);
            speak(currentLang === 'hi'
                ? `${getPageNameHi(page)} खोल रहे हैं`
                : `Opening ${page}`
            );
            showToast(`🎤 → ${page}`);
            return;
        }
    }

    // No command recognized
    document.getElementById('voice-status').textContent = currentLang === 'hi'
        ? 'समझ नहीं आया, दोबारा बोलें...'
        : 'Didn\'t understand, try again...';
}

function handleVoiceError(event) {
    console.error('Voice error:', event.error);

    if (event.error === 'no-speech') {
        document.getElementById('voice-status').textContent = currentLang === 'hi'
            ? 'कोई आवाज़ नहीं सुनाई दी'
            : 'No speech detected';
    } else if (event.error === 'not-allowed') {
        showToast('❌ Microphone permission denied');
        stopVoice();
    }
}

function handleVoiceEnd() {
    if (isListening) {
        // Restart if we're still supposed to be listening
        try { recognition.start(); } catch (e) { }
    }
}

function getPageNameHi(page) {
    const names = {
        'dashboard': 'डैशबोर्ड',
        'scanner': 'रोग स्कैनर',
        'ledger': 'खेत-खाता',
        'mandi': 'मंडी भाव',
        'weather': 'मौसम अलर्ट',
        'certificate': 'प्रमाणपत्र'
    };
    return names[page] || page;
}

// Text-to-Speech
function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = currentLang === 'hi' ? 'hi-IN' : 'en-IN';
        utterance.rate = 0.9;
        speechSynthesis.speak(utterance);
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    setTimeout(initVoice, 3000); // Init after splash
});
