"""
Management command to seed phoneme data.

Loads the 44 English phonemes into the database.
Run with: python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from apps.library.models import Phoneme, ReferenceSentence


class Command(BaseCommand):
    help = 'Seed database with English phonemes and initial data'
    
    def handle(self, *args, **options):
        self.stdout.write('Seeding phoneme data...')
        
        phonemes_created = self.seed_phonemes()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {phonemes_created} phonemes')
        )
        
        self.stdout.write('Seeding reference sentences...')
        sentences_created = self.seed_sentences()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {sentences_created} sentences')
        )
    
    def seed_phonemes(self):
        """Seed all 44 English phonemes."""
        
        phonemes_data = [
            # Vowels
            {'symbol': '/i/', 'arpabet': 'IY', 'ipa': 'i', 'type': 'vowel', 'example_word': 'see', 'description': 'High front tense vowel'},
            {'symbol': '/ɪ/', 'arpabet': 'IH', 'ipa': 'ɪ', 'type': 'vowel', 'example_word': 'sit', 'description': 'High front lax vowel'},
            {'symbol': '/e/', 'arpabet': 'EY', 'ipa': 'eɪ', 'type': 'diphthong', 'example_word': 'say', 'description': 'Mid front diphthong'},
            {'symbol': '/ɛ/', 'arpabet': 'EH', 'ipa': 'ɛ', 'type': 'vowel', 'example_word': 'bed', 'description': 'Mid front lax vowel'},
            {'symbol': '/æ/', 'arpabet': 'AE', 'ipa': 'æ', 'type': 'vowel', 'example_word': 'cat', 'description': 'Low front vowel'},
            {'symbol': '/ɑ/', 'arpabet': 'AA', 'ipa': 'ɑ', 'type': 'vowel', 'example_word': 'father', 'description': 'Low back vowel'},
            {'symbol': '/ɔ/', 'arpabet': 'AO', 'ipa': 'ɔ', 'type': 'vowel', 'example_word': 'thought', 'description': 'Mid back rounded vowel'},
            {'symbol': '/o/', 'arpabet': 'OW', 'ipa': 'oʊ', 'type': 'diphthong', 'example_word': 'go', 'description': 'Mid back diphthong'},
            {'symbol': '/ʊ/', 'arpabet': 'UH', 'ipa': 'ʊ', 'type': 'vowel', 'example_word': 'book', 'description': 'High back lax vowel'},
            {'symbol': '/u/', 'arpabet': 'UW', 'ipa': 'u', 'type': 'vowel', 'example_word': 'too', 'description': 'High back tense vowel'},
            {'symbol': '/ʌ/', 'arpabet': 'AH', 'ipa': 'ʌ', 'type': 'vowel', 'example_word': 'but', 'description': 'Mid central vowel'},
            {'symbol': '/ə/', 'arpabet': 'AX', 'ipa': 'ə', 'type': 'vowel', 'example_word': 'about', 'description': 'Schwa (reduced vowel)'},
            {'symbol': '/ɝ/', 'arpabet': 'ER', 'ipa': 'ɝ', 'type': 'vowel', 'example_word': 'bird', 'description': 'R-colored vowel'},
            
            # Diphthongs
            {'symbol': '/aɪ/', 'arpabet': 'AY', 'ipa': 'aɪ', 'type': 'diphthong', 'example_word': 'my', 'description': 'Low front to high diphthong'},
            {'symbol': '/aʊ/', 'arpabet': 'AW', 'ipa': 'aʊ', 'type': 'diphthong', 'example_word': 'how', 'description': 'Low to high back diphthong'},
            {'symbol': '/ɔɪ/', 'arpabet': 'OY', 'ipa': 'ɔɪ', 'type': 'diphthong', 'example_word': 'boy', 'description': 'Mid back to high front diphthong'},
            
            # Plosives (Stops)
            {'symbol': '/p/', 'arpabet': 'P', 'ipa': 'p', 'type': 'plosive', 'example_word': 'pen', 'description': 'Voiceless bilabial plosive'},
            {'symbol': '/b/', 'arpabet': 'B', 'ipa': 'b', 'type': 'plosive', 'example_word': 'bad', 'description': 'Voiced bilabial plosive'},
            {'symbol': '/t/', 'arpabet': 'T', 'ipa': 't', 'type': 'plosive', 'example_word': 'ten', 'description': 'Voiceless alveolar plosive'},
            {'symbol': '/d/', 'arpabet': 'D', 'ipa': 'd', 'type': 'plosive', 'example_word': 'day', 'description': 'Voiced alveolar plosive'},
            {'symbol': '/k/', 'arpabet': 'K', 'ipa': 'k', 'type': 'plosive', 'example_word': 'key', 'description': 'Voiceless velar plosive'},
            {'symbol': '/g/', 'arpabet': 'G', 'ipa': 'g', 'type': 'plosive', 'example_word': 'go', 'description': 'Voiced velar plosive'},
            
            # Fricatives
            {'symbol': '/f/', 'arpabet': 'F', 'ipa': 'f', 'type': 'fricative', 'example_word': 'fan', 'description': 'Voiceless labiodental fricative'},
            {'symbol': '/v/', 'arpabet': 'V', 'ipa': 'v', 'type': 'fricative', 'example_word': 'van', 'description': 'Voiced labiodental fricative'},
            {'symbol': '/θ/', 'arpabet': 'TH', 'ipa': 'θ', 'type': 'fricative', 'example_word': 'think', 'description': 'Voiceless dental fricative'},
            {'symbol': '/ð/', 'arpabet': 'DH', 'ipa': 'ð', 'type': 'fricative', 'example_word': 'this', 'description': 'Voiced dental fricative'},
            {'symbol': '/s/', 'arpabet': 'S', 'ipa': 's', 'type': 'fricative', 'example_word': 'see', 'description': 'Voiceless alveolar fricative'},
            {'symbol': '/z/', 'arpabet': 'Z', 'ipa': 'z', 'type': 'fricative', 'example_word': 'zoo', 'description': 'Voiced alveolar fricative'},
            {'symbol': '/ʃ/', 'arpabet': 'SH', 'ipa': 'ʃ', 'type': 'fricative', 'example_word': 'she', 'description': 'Voiceless postalveolar fricative'},
            {'symbol': '/ʒ/', 'arpabet': 'ZH', 'ipa': 'ʒ', 'type': 'fricative', 'example_word': 'measure', 'description': 'Voiced postalveolar fricative'},
            {'symbol': '/h/', 'arpabet': 'HH', 'ipa': 'h', 'type': 'fricative', 'example_word': 'hat', 'description': 'Voiceless glottal fricative'},
            
            # Affricates
            {'symbol': '/tʃ/', 'arpabet': 'CH', 'ipa': 'tʃ', 'type': 'affricate', 'example_word': 'chin', 'description': 'Voiceless postalveolar affricate'},
            {'symbol': '/dʒ/', 'arpabet': 'JH', 'ipa': 'dʒ', 'type': 'affricate', 'example_word': 'jam', 'description': 'Voiced postalveolar affricate'},
            
            # Nasals
            {'symbol': '/m/', 'arpabet': 'M', 'ipa': 'm', 'type': 'nasal', 'example_word': 'man', 'description': 'Bilabial nasal'},
            {'symbol': '/n/', 'arpabet': 'N', 'ipa': 'n', 'type': 'nasal', 'example_word': 'no', 'description': 'Alveolar nasal'},
            {'symbol': '/ŋ/', 'arpabet': 'NG', 'ipa': 'ŋ', 'type': 'nasal', 'example_word': 'sing', 'description': 'Velar nasal'},
            
            # Liquids
            {'symbol': '/l/', 'arpabet': 'L', 'ipa': 'l', 'type': 'liquid', 'example_word': 'leg', 'description': 'Alveolar lateral approximant'},
            {'symbol': '/r/', 'arpabet': 'R', 'ipa': 'ɹ', 'type': 'liquid', 'example_word': 'red', 'description': 'Alveolar approximant'},
            
            # Glides (Semivowels)
            {'symbol': '/w/', 'arpabet': 'W', 'ipa': 'w', 'type': 'glide', 'example_word': 'we', 'description': 'Labial-velar approximant'},
            {'symbol': '/j/', 'arpabet': 'Y', 'ipa': 'j', 'type': 'glide', 'example_word': 'yes', 'description': 'Palatal approximant'},
        ]
        
        # Add articulation tips
        tips = {
            'TH': 'Place tongue tip between teeth, blow air gently without voice.',
            'DH': 'Same as TH but add voice from your throat.',
            'R': 'Curl tongue tip back slightly, do not touch roof of mouth.',
            'L': 'Touch tongue tip to ridge behind upper front teeth.',
            'SH': 'Round lips slightly, push air through wide channel.',
            'CH': 'Start with tongue at roof, release with SH sound.',
            'S': 'Tongue behind teeth, narrow air channel, no voice.',
            'Z': 'Same as S but with voice.',
            'NG': 'Back of tongue touches soft palate, air through nose.',
            'W': 'Round lips tightly, glide to next vowel.',
            'V': 'Gently bite lower lip, blow air with voice.',
            'F': 'Same as V but without voice.',
        }
        
        created_count = 0
        for data in phonemes_data:
            data['articulation_tip'] = tips.get(data['arpabet'], '')
            phoneme, created = Phoneme.objects.update_or_create(
                arpabet=data['arpabet'],
                defaults=data
            )
            if created:
                created_count += 1
        
        return created_count
    
    def seed_sentences(self):
        """Seed reference sentences for practice."""
        
        sentences_data = [
            # Beginner sentences
            {
                'text': 'The cat sat on the mat.',
                'difficulty_level': 'beginner',
                'phoneme_sequence': ['DH', 'AH', 'K', 'AE', 'T', 'S', 'AE', 'T', 'AA', 'N', 'DH', 'AH', 'M', 'AE', 'T'],
                'alignment_map': [],
                'target_phonemes': ['TH', 'AE', 'T'],
                'source': 'curated',
            },
            {
                'text': 'She sells sea shells.',
                'difficulty_level': 'beginner',
                'phoneme_sequence': ['SH', 'IY', 'S', 'EH', 'L', 'Z', 'S', 'IY', 'SH', 'EH', 'L', 'Z'],
                'alignment_map': [],
                'target_phonemes': ['SH', 'S', 'L'],
                'source': 'curated',
            },
            {
                'text': 'The sun is very hot.',
                'difficulty_level': 'beginner',
                'phoneme_sequence': ['DH', 'AH', 'S', 'AH', 'N', 'IH', 'Z', 'V', 'EH', 'R', 'IY', 'HH', 'AA', 'T'],
                'alignment_map': [],
                'target_phonemes': ['S', 'V', 'R'],
                'source': 'curated',
            },
            {
                'text': 'I like to read books.',
                'difficulty_level': 'beginner',
                'phoneme_sequence': ['AY', 'L', 'AY', 'K', 'T', 'UW', 'R', 'IY', 'D', 'B', 'UH', 'K', 'S'],
                'alignment_map': [],
                'target_phonemes': ['L', 'R', 'K'],
                'source': 'curated',
            },
            {
                'text': 'The dog runs fast.',
                'difficulty_level': 'beginner',
                'phoneme_sequence': ['DH', 'AH', 'D', 'AO', 'G', 'R', 'AH', 'N', 'Z', 'F', 'AE', 'S', 'T'],
                'alignment_map': [],
                'target_phonemes': ['D', 'G', 'F'],
                'source': 'curated',
            },
            {
                'text': 'Please pass the water.',
                'difficulty_level': 'beginner',
                'phoneme_sequence': ['P', 'L', 'IY', 'Z', 'P', 'AE', 'S', 'DH', 'AH', 'W', 'AO', 'T', 'ER'],
                'alignment_map': [],
                'target_phonemes': ['P', 'W', 'Z'],
                'source': 'curated',
            },
            # Intermediate sentences
            {
                'text': 'The weather today is particularly pleasant.',
                'difficulty_level': 'intermediate',
                'phoneme_sequence': ['DH', 'AH', 'W', 'EH', 'DH', 'ER', 'T', 'AH', 'D', 'EY', 'IH', 'Z', 'P', 'ER', 'T', 'IH', 'K', 'Y', 'AH', 'L', 'ER', 'L', 'IY', 'P', 'L', 'EH', 'Z', 'AH', 'N', 'T'],
                'alignment_map': [],
                'target_phonemes': ['TH', 'DH', 'L', 'Y'],
                'source': 'curated',
            },
            {
                'text': 'She thought thoroughly about the theory.',
                'difficulty_level': 'intermediate',
                'phoneme_sequence': ['SH', 'IY', 'TH', 'AO', 'T', 'TH', 'ER', 'OW', 'L', 'IY', 'AH', 'B', 'AW', 'T', 'DH', 'AH', 'TH', 'IY', 'ER', 'IY'],
                'alignment_map': [],
                'target_phonemes': ['TH', 'SH', 'R'],
                'source': 'curated',
            },
            {
                'text': 'The restaurant serves excellent cuisine.',
                'difficulty_level': 'intermediate',
                'phoneme_sequence': ['DH', 'AH', 'R', 'EH', 'S', 'T', 'ER', 'AA', 'N', 'T', 'S', 'ER', 'V', 'Z', 'EH', 'K', 'S', 'AH', 'L', 'AH', 'N', 'T', 'K', 'W', 'IH', 'Z', 'IY', 'N'],
                'alignment_map': [],
                'target_phonemes': ['R', 'S', 'Z'],
                'source': 'curated',
            },
            {
                'text': 'Practice makes perfect pronunciation.',
                'difficulty_level': 'intermediate',
                'phoneme_sequence': ['P', 'R', 'AE', 'K', 'T', 'IH', 'S', 'M', 'EY', 'K', 'S', 'P', 'ER', 'F', 'IH', 'K', 'T', 'P', 'R', 'AH', 'N', 'AH', 'N', 'S', 'IY', 'EY', 'SH', 'AH', 'N'],
                'alignment_map': [],
                'target_phonemes': ['P', 'R', 'K'],
                'source': 'curated',
            },
            {
                'text': 'Children love playing in the garden.',
                'difficulty_level': 'intermediate',
                'phoneme_sequence': ['CH', 'IH', 'L', 'D', 'R', 'AH', 'N', 'L', 'AH', 'V', 'P', 'L', 'EY', 'IH', 'NG', 'IH', 'N', 'DH', 'AH', 'G', 'AA', 'R', 'D', 'AH', 'N'],
                'alignment_map': [],
                'target_phonemes': ['CH', 'NG', 'G'],
                'source': 'curated',
            },
            {
                'text': 'The musician played beautiful melodies.',
                'difficulty_level': 'intermediate',
                'phoneme_sequence': ['DH', 'AH', 'M', 'Y', 'UW', 'Z', 'IH', 'SH', 'AH', 'N', 'P', 'L', 'EY', 'D', 'B', 'Y', 'UW', 'T', 'AH', 'F', 'AH', 'L', 'M', 'EH', 'L', 'AH', 'D', 'IY', 'Z'],
                'alignment_map': [],
                'target_phonemes': ['M', 'Y', 'Z'],
                'source': 'curated',
            },
            # Advanced sentences
            {
                'text': 'The quintessential characteristics of sophisticated articulation require diligent practice.',
                'difficulty_level': 'advanced',
                'phoneme_sequence': ['DH', 'AH', 'K', 'W', 'IH', 'N', 'T', 'EH', 'S', 'EH', 'N', 'SH', 'AH', 'L', 'K', 'EH', 'R', 'AH', 'K', 'T', 'ER', 'IH', 'S', 'T', 'IH', 'K', 'S', 'AH', 'V', 'S', 'AH', 'F', 'IH', 'S', 'T', 'IH', 'K', 'EY', 'T', 'IH', 'D', 'AA', 'R', 'T', 'IH', 'K', 'Y', 'AH', 'L', 'EY', 'SH', 'AH', 'N'],
                'alignment_map': [],
                'target_phonemes': ['K', 'SH', 'T'],
                'source': 'curated',
            },
            {
                'text': 'Throughout the archaeological excavation, researchers discovered extraordinary artifacts.',
                'difficulty_level': 'advanced',
                'phoneme_sequence': ['TH', 'R', 'UW', 'AW', 'T', 'DH', 'AH', 'AA', 'R', 'K', 'IY', 'AH', 'L', 'AA', 'JH', 'IH', 'K', 'AH', 'L', 'EH', 'K', 'S', 'K', 'AH', 'V', 'EY', 'SH', 'AH', 'N'],
                'alignment_map': [],
                'target_phonemes': ['TH', 'R', 'JH'],
                'source': 'curated',
            },
            {
                'text': 'The enthusiastic entrepreneur established an innovative enterprise.',
                'difficulty_level': 'advanced',
                'phoneme_sequence': ['DH', 'AH', 'IH', 'N', 'TH', 'UW', 'Z', 'IY', 'AE', 'S', 'T', 'IH', 'K', 'AA', 'N', 'T', 'R', 'AH', 'P', 'R', 'AH', 'N', 'ER'],
                'alignment_map': [],
                'target_phonemes': ['TH', 'Z', 'N'],
                'source': 'curated',
            },
            {
                'text': 'Philosophical perspectives perpetually provoke profound contemplation.',
                'difficulty_level': 'advanced',
                'phoneme_sequence': ['F', 'IH', 'L', 'AH', 'S', 'AA', 'F', 'IH', 'K', 'AH', 'L', 'P', 'ER', 'S', 'P', 'EH', 'K', 'T', 'IH', 'V', 'Z'],
                'alignment_map': [],
                'target_phonemes': ['F', 'L', 'P'],
                'source': 'curated',
            },
            {
                'text': 'The distinguished gentleman demonstrated remarkable rhetorical skills.',
                'difficulty_level': 'advanced',
                'phoneme_sequence': ['DH', 'AH', 'D', 'IH', 'S', 'T', 'IH', 'NG', 'G', 'W', 'IH', 'SH', 'T', 'JH', 'EH', 'N', 'T', 'AH', 'L', 'M', 'AH', 'N'],
                'alignment_map': [],
                'target_phonemes': ['NG', 'JH', 'R'],
                'source': 'curated',
            },
            {
                'text': 'Simultaneously synthesizing sophisticated solutions requires exceptional expertise.',
                'difficulty_level': 'advanced',
                'phoneme_sequence': ['S', 'AY', 'M', 'AH', 'L', 'T', 'EY', 'N', 'IY', 'AH', 'S', 'L', 'IY', 'S', 'IH', 'N', 'TH', 'AH', 'S', 'AY', 'Z', 'IH', 'NG'],
                'alignment_map': [],
                'target_phonemes': ['S', 'TH', 'Z'],
                'source': 'curated',
            },
        ]
        
        created_count = 0
        for data in sentences_data:
            sentence, created = ReferenceSentence.objects.update_or_create(
                text=data['text'],
                defaults={
                    'difficulty_level': data['difficulty_level'],
                    'phoneme_sequence': data['phoneme_sequence'],
                    'alignment_map': data['alignment_map'],
                    'target_phonemes': data['target_phonemes'],
                    'source': data['source'],
                    'is_validated': True,
                }
            )
            if created:
                created_count += 1
        
        return created_count
