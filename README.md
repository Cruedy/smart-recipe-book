# Smart Recipe Book
## Intro
I created a Smart Recipe Book, this is particularly useful for me because when I cook, I like to consider how healthy the recipes that I'm cooking are. This is usually a pretty tedious process because I have to measure each ingredient from the recipe, then look up the nutritional facts of each ingredient, then add up the nutritional facts. This website allows me to filter out recipes that already don't fit my needs nutritionally.

### How I used Greptile
I used Greptile as a rate limit checker for my backend code. I'm using the Fat Secret Platform API:
https://platform.fatsecret.com/docs/v4/food.get
which has a rate limit of 5,000 calls per day. In my code, I have to make over 5,000 calls to the api in order to gather information. Ive decreased the number of times this has to be done by gathering the information from the Fat Secret API, and creating a json file called `recipes.json`. Is all written in `rateLimitMonitor.py`. Greptile is used to check the code base and find out what the rate limit of the Fat Secret API is, and find out when I can next call the API once the rate limit has been met.

In addition to this, I also queried Greptile to generate a developer guide for this codebase and add it to this `ReadMe.md` in markdown format.

### APIs used
[Greptile](https://docs.greptile.com/introduction)
[MealDB](https://www.themealdb.com/api.php)
[FatSecret](https://link-url-here.org)

### Extra Tools used
I ran into a couple environment errors for running some of the libraries I used, so I used ChatGPT and Google to resolve those issues.

### Special Concepts Used
#### Regular Expressions
In the files `ingredientSearch.py` and `rateLimitMonitor.py` I used regular expressions to parse large amounts of data in order to get the strings I needed.

#### Multithreading/Concurrency
In the file `recipeSearch.py`, I used multithreading to speed up the process of getting all recipes in the function `getAllRecipes()`. I did this by allowing 5 calls to happen at the same time, which reduces the amount of individual time that each call takes.

### How to start backend
cd myapp
source .venv/bin/activate
flask run

## Getting Started with Create React App

This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).

### Available Scripts

In the project directory, you can run:

#### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

#### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

#### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

#### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

### Learn More

You can learn more in the [Create React App documentation](https://facebook.github.io/create-react-app/docs/getting-started).

To learn React, check out the [React documentation](https://reactjs.org/).

#### Code Splitting

This section has moved here: [https://facebook.github.io/create-react-app/docs/code-splitting](https://facebook.github.io/create-react-app/docs/code-splitting)

#### Analyzing the Bundle Size

This section has moved here: [https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size](https://facebook.github.io/create-react-app/docs/analyzing-the-bundle-size)

#### Making a Progressive Web App

This section has moved here: [https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app](https://facebook.github.io/create-react-app/docs/making-a-progressive-web-app)

#### Advanced Configuration

This section has moved here: [https://facebook.github.io/create-react-app/docs/advanced-configuration](https://facebook.github.io/create-react-app/docs/advanced-configuration)

#### Deployment

This section has moved here: [https://facebook.github.io/create-react-app/docs/deployment](https://facebook.github.io/create-react-app/docs/deployment)

#### `npm run build` fails to minify

This section has moved here: [https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify](https://facebook.github.io/create-react-app/docs/troubleshooting#npm-run-build-fails-to-minify)

## Developer Guide(Generated by Greptile)
### Code Description
#### /myapp/api.py
The `/myapp/api.py` file defines a Flask web application that provides an API endpoint for filtering and returning recipes based on nutritional criteria and ingredients. It utilizes CORS for cross-origin requests and includes a rate limit monitoring feature.

##### Overall Summary
The file sets up a Flask application with a single API endpoint (`/api/route`) that processes POST requests to filter recipes based on nutritional criteria and a specified ingredient. It reads from a `recipes.json` file and uses a helper function to retrieve recipe details.

##### Class and Function Summaries

- **`app`**: An instance of the Flask application, which serves as the main entry point for handling web requests.

- **`rate_monitor`**: An instance of the `RateLimitMonitor` class, which is presumably used to track and manage the rate of incoming requests to the API.

- **`@app.route('/api/route', methods=['POST'])`**: A decorator that defines the `/api/route` endpoint, which accepts POST requests.

- **`returnFoodList()`**: A function that processes a JSON request to filter and return a list of recipes based on specified nutritional criteria (calories, fat, carbs, protein) and an ingredient. It reads from a `recipes.json` file and utilizes the helper function `fromIngredient`.

- **`fromIngredient(ingredient)`**: A helper function that takes an `ingredient` as input, retrieves recipe details (names, links, images, and IDs) using the `searchRecipe` function, and constructs a list of recipes, where each recipe is represented as a list containing the name, link, image, and ID.
ing**:
  - `.catch(error => console.error('Error:', error));`
    - Catches and logs any errors that occur during the fetch request or response processing.
 piece of text.
ody>`**: Contains the content of the document.

- **`<noscript>You need to enable JavaScript to run this app.</noscript>`**: Displays a message if JavaScript is disabled in the user's browser.

- **`<div id="root"></div>`**: A placeholder div where the React application will be rendered.

- **Comments**: Provide additional context about the file's purpose, usage of `%PUBLIC_URL%`, and instructions for development and production builds.
 Python virtual environments, as well as provide command-line tools for package management and character encoding detection.
 deployment of the Flask application, with a focus on maintaining a clean and organized codebase.
ic, and testing configurations, facilitating a clean and maintainable codebase.
*: Contains functional components (`Filter.jsx` and `SearchBars.jsx`).
     - **`index.css`**: Default styles for the application.
     - **`index.js`**: Entry point for the React app.
     - **`reportWebVitals.js`**: Function for reporting web performance metrics.
     - **`setupTests.js`**: Configures the testing environment for Jest.

### Overall Functionality
The project integrates a Flask backend for recipe management and a React frontend for user interaction, utilizing external APIs for data retrieval and management. It is structured for maintainability and ease of development, with clear separation of concerns across different components and scripts.
