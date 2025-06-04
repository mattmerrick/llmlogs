# LLM API Documentation

## Overview
This API provides comprehensive, up-to-date information about Large Language Models (LLMs) in a clean, structured JSON format. The API is designed to be easily integrated into applications, plugins, and extensions.

## Endpoint
```
GET https://llmlogs.com/api/llms.json
```

## Data Structure

### Root Object
```json
{
  "version": "string",
  "last_updated": "string (YYYY-MM-DD)",
  "models": object,
  "metadata": object
}
```

### Model Object
Each model contains:
- `provider`: Company providing the model
- `name`: Display name of the model
- `versions`: Array of version objects
- `capabilities`: Array of supported features
- `documentation_url`: Link to official documentation

### Version Object
Each version contains:
- `name`: Specific version identifier
- `context_window`: Maximum context length
- `release_date`: Release date (YYYY-MM-DD)
- `pricing`: Pricing information object

### Pricing Object
- `input`: Cost per input unit
- `output`: Cost per output unit
- `unit`: Pricing unit (e.g., "1K tokens")
- `currency`: Currency code

## Example Usage

### JavaScript
```javascript
async function getLLMData() {
  const response = await fetch('https://llmlogs.com/api/llms.json');
  const data = await response.json();
  return data;
}
```

### Python
```python
import requests

def get_llm_data():
    response = requests.get('https://llmlogs.com/api/llms.json')
    return response.json()
```

## Features
- ✅ Comprehensive model information
- ✅ Up-to-date pricing data
- ✅ Detailed capability descriptions
- ✅ Version history tracking
- ✅ Official documentation links

## Use Cases
1. Cost calculators
2. LLM comparison tools
3. Model selection assistants
4. Documentation and tutorials
5. Research and analysis

## Updates
The API is updated regularly as new models are released or existing models are updated. Check the `last_updated` field for the most recent update date.

## Contributing
Found an error or want to add a new model? Submit a pull request or issue on our [GitHub repository](https://github.com/mattmerrick/llmseoguide).

## License
This API is provided under the MIT License. You're free to use it in your projects, both commercial and non-commercial. 