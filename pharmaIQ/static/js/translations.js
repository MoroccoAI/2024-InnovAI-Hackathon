let translations = {
    'en': {},
    'ar': {}
};

function translatePage(lang) {
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (!translations[lang][key]) {
            // If translation doesn't exist, add the original text
            translations[lang][key] = element.textContent;
        }
        element.textContent = translations[lang][key];
    });

    document.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;

    if (lang === 'ar' && Object.keys(translations['ar']).length === 0) {
        // If Arabic translations are empty, use Google Translate
        googleTranslateElementInit();
    }
}

function googleTranslateElementInit() {
    new google.translate.TranslateElement({
        pageLanguage: 'en',
        includedLanguages: 'ar',
        autoDisplay: false
    }, 'google_translate_element');

    // Wait for translation to complete
    setTimeout(() => {
        // Collect translations
        document.querySelectorAll('[data-translate]').forEach(element => {
            const key = element.getAttribute('data-translate');
            translations['ar'][key] = element.textContent;
        });

        // Remove Google Translate elements
        const googleTranslateElement = document.getElementById('google_translate_element');
        if (googleTranslateElement) {
            googleTranslateElement.remove();
        }
        const googleTranslateElementStyle = document.getElementById(':0.targetLanguage');
        if (googleTranslateElementStyle) {
            googleTranslateElementStyle.remove();
        }

        // Save translations to localStorage
        localStorage.setItem('translations', JSON.stringify(translations));

        console.log('Translations saved:', translations);
    }, 2000); // Adjust timeout as needed
}

// Load saved translations from localStorage
const savedTranslations = localStorage.getItem('translations');
if (savedTranslations) {
    translations = JSON.parse(savedTranslations);
}