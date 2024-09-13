require('dotenv').config();

const greptile_api_key = process.env.greptile_api_key;
const github_token = process.env.PAT;

const repository_identifier = encodeURIComponent("github:main:pandas-dev/pandas");

fetch(`https://api.greptile.com/v2/repositories/${repository_identifier}`, {
    method: 'GET',
    headers: {
        'Authorization': `Bearer ${greptile_api_key}`,
        'X-Github-Token': github_token
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));