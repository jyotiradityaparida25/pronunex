# Contributing to Pronunex

Thank you for your interest in contributing to Pronunex. This document provides guidelines and best practices for contributing to the project.

## Code of Conduct

- Be respectful and professional
- Welcome newcomers and help them get started
- Focus on constructive feedback
- Respect different viewpoints and experiences

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Set up the development environment (see README.md)
4. Create a new branch for your feature or fix
5. Make your changes
6. Test thoroughly
7. Submit a pull request

## Architecture Principles

Pronunex follows strict architectural guidelines to maintain scientific validity and production-grade quality:

### 1. Separation of Concerns

- **NLP Core** handles signal processing only
- **LLM Engine** generates feedback text only
- Never mix pronunciation scoring with LLM logic

### 2. Deterministic Scoring

- All pronunciation scores use cosine similarity on embeddings
- No subjective or probabilistic scoring
- Thresholds are configurable and documented

### 3. LLM Constraints

**ALLOWED:**
- Generating human-readable feedback text
- Creating practice sentences (with G2P validation)
- Explaining recommendations
- Conversational coaching

**PROHIBITED:**
- Scoring pronunciation
- Detecting phonemes
- Judging speech correctness

### 4. Data Integrity

- Reference phonemes and embeddings are precomputed and cached
- User data and reference data are never mixed
- All LLM outputs are validated before use

## Development Workflow

### Branch Naming

Use descriptive branch names:

- `feature/add-phoneme-filtering`
- `fix/audio-upload-bug`
- `docs/update-api-documentation`
- `refactor/improve-scoring-logic`

### Commit Messages

Follow conventional commit format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples:**

```
feat(practice): add phoneme-level progress tracking

Implement detailed phoneme progress tracking with historical
data and trend analysis.

Closes #123
```

```
fix(assessment): correct alignment timestamp calculation

Fixed off-by-one error in phoneme timestamp extraction
that caused incorrect audio slicing.
```

### Code Style

#### Backend (Python)

- Follow PEP 8 style guide
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused
- Use type hints where appropriate

**Example:**

```python
def calculate_phoneme_score(
    user_embedding: np.ndarray,
    reference_embedding: np.ndarray
) -> float:
    """
    Calculate pronunciation score using cosine similarity.
    
    Args:
        user_embedding: User audio embedding (768-dim)
        reference_embedding: Reference audio embedding (768-dim)
    
    Returns:
        Similarity score between 0 and 1
    """
    return cosine_similarity(user_embedding, reference_embedding)
```

#### Frontend (JavaScript/React)

- Use ESLint and Prettier configurations
- Use functional components with hooks
- Keep components small and reusable
- Use meaningful prop names
- Add PropTypes or TypeScript types

**Example:**

```javascript
/**
 * Display phoneme card with articulation tips
 */
function PhonemeCard({ phoneme, onClick }) {
  return (
    <div className="phoneme-card" onClick={() => onClick(phoneme)}>
      <h3>{phoneme.arpabet}</h3>
      <p>{phoneme.articulation_tip}</p>
    </div>
  );
}
```

## Testing Requirements

### Backend Tests

- Write unit tests for new functions
- Test edge cases and error conditions
- Maintain test coverage above 80%

```bash
# Run tests
python manage.py test

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

### Frontend Tests

Currently manual testing is used. Future contributions should include:

- Component tests using React Testing Library
- Integration tests for user flows
- E2E tests using Cypress

## Pull Request Process

1. **Update Documentation**: Update README and relevant docs
2. **Add Tests**: Include tests for new features
3. **Run Linters**: Ensure code passes linting
4. **Test Locally**: Verify everything works
5. **Write Clear Description**: Explain what and why
6. **Reference Issues**: Link related issues
7. **Request Review**: Tag relevant reviewers

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-reviewed the code
- [ ] Commented complex logic
- [ ] Updated documentation
- [ ] Added tests
- [ ] All tests pass
- [ ] No new warnings

## Related Issues
Closes #123
```

## Adding New Features

### Backend Features

1. **Plan the Architecture**: Ensure it fits the separation of concerns
2. **Create Models**: Add database models if needed
3. **Write Business Logic**: Implement in appropriate service/module
4. **Create API Endpoints**: Add REST endpoints
5. **Write Tests**: Unit and integration tests
6. **Update Documentation**: API docs and README

### Frontend Features

1. **Design the UI**: Sketch or wireframe first
2. **Create Components**: Build reusable components
3. **Implement State**: Use Context or local state
4. **Connect to API**: Integrate with backend
5. **Style**: Follow design system
6. **Test**: Manual testing (automated in future)
7. **Update Documentation**: Component usage and props

## Common Tasks

### Adding a New Phoneme

```python
from apps.library.models import Phoneme

Phoneme.objects.create(
    arpabet='AE',
    ipa='æ',
    example_word='cat',
    articulation_tip='Lower jaw, spread lips, tongue low'
)
```

### Adding a Reference Sentence

```python
from apps.library.models import ReferenceSentence

sentence = ReferenceSentence.objects.create(
    text='The cat sat on the mat',
    difficulty='beginner'
)

# Precompute phonemes and embeddings
sentence.precompute_data()
```

### Creating a New API Endpoint

```python
# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def my_endpoint(request):
    data = {'message': 'Hello'}
    return Response(data)

# urls.py
urlpatterns = [
    path('my-endpoint/', views.my_endpoint),
]
```

## LLM Integration Guidelines

When working with LLM features:

1. **Use Structured Prompts**: Define clear, constrained prompts
2. **Validate Outputs**: Always validate LLM responses
3. **Provide Fallbacks**: Handle API failures gracefully
4. **Log Usage**: Track LLM calls for debugging
5. **Never Trust Blindly**: Verify all LLM outputs

**Example:**

```python
from services.llm_service import LLMService

def generate_feedback(weak_phonemes):
    prompt = f"""
    Generate feedback for these weak phonemes: {weak_phonemes}
    
    Rules:
    - Be encouraging
    - Provide specific tips
    - Keep it under 100 words
    """
    
    llm = LLMService()
    feedback = llm.generate(prompt)
    
    # Validate output
    if not feedback or len(feedback) > 500:
        return "Keep practicing! Focus on these sounds."
    
    return feedback
```

## Documentation Standards

- Keep README files up to date
- Document all API endpoints
- Add inline comments for complex logic
- Use docstrings for functions and classes
- Update architecture docs when changing structure

## Questions and Support

- **Issues**: Use GitHub Issues for bugs and features
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact maintainers for sensitive issues

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Recognition

Contributors will be recognized in:
- GitHub contributors page
- Project documentation
- Release notes

Thank you for contributing to Pronunex!
