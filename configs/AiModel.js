const {
    GoogleGenerativeAI,
    HarmCategory,
    HarmBlockThreshold,
  } = require("@google/generative-ai");
  
  const apiKey = process.env.NEXT_PUBLIC_GEMINI_API_KEY;
  const genAI = new GoogleGenerativeAI(apiKey);
  
  const model = genAI.getGenerativeModel({
    model: "gemini-1.5-flash-002",
  });
  
  const generationConfig = {
    temperature: 1,
    topP: 0.95,
    topK: 40,
    maxOutputTokens: 8192,
    responseMimeType: "application/json",
  };

  const generationConfig2 = {
    temperature: 1,
    topP: 0.95,
    topK: 40,
    maxOutputTokens: 8192,
    responseMimeType: "text/plain",
  };
  

    export const courseOutlineAIModel = model.startChat({
      generationConfig,
      history: [
        {
          role: "user",
          parts: [
            {text: "Generate a study material for Python for  Exam and level of difficulty will be EASY with summery of course,List of Chapters along with summery for each chapter, Topic list in each chapter, All resule in JSON format\n\n"},
          ],
        },
        {
          role: "model",
          parts: [
            {text: "```json\n{\n  \"course_title\": \"Python for Beginners\",\n  \"difficulty\": \"Easy\",\n  \"summary\": \"This course provides an introduction to the Python programming language, covering the fundamentals necessary to write simple programs and understand basic programming concepts.\",\n  \"chapters\": [\n    {\n      \"chapter_title\": \"Introduction to Python\",\n      \"summary\": \"This chapter introduces the Python programming language, its history, and its uses. It also covers basic syntax and the concept of variables and data types.\",\n      \"topics\": [\n        \"What is Python?\",\n        \"Why use Python?\",\n        \"Installing Python\",\n        \"Running Python code\",\n        \"Basic syntax\",\n        \"Variables and data types\",\n        \"Operators\"\n      ]\n    },\n    {\n      \"chapter_title\": \"Control Flow\",\n      \"summary\": \"This chapter focuses on controlling the flow of execution in Python programs, including conditional statements, loops, and functions.\",\n      \"topics\": [\n        \"Conditional statements (if, elif, else)\",\n        \"Loops (for, while)\",\n        \"Loop control statements (break, continue)\",\n        \"Functions\"\n      ]\n    },\n    {\n      \"chapter_title\": \"Data Structures\",\n      \"summary\": \"This chapter introduces fundamental data structures in Python, such as lists, tuples, dictionaries, and sets.\",\n      \"topics\": [\n        \"Lists\",\n        \"Tuples\",\n        \"Dictionaries\",\n        \"Sets\"\n      ]\n    },\n    {\n      \"chapter_title\": \"Strings and Input/Output\",\n      \"summary\": \"This chapter covers working with strings, taking input from the user, and displaying output in Python programs.\",\n      \"topics\": [\n        \"String manipulation\",\n        \"String formatting\",\n        \"Input and output (input(), print())\"\n      ]\n    },\n    {\n      \"chapter_title\": \"Modules and Libraries\",\n      \"summary\": \"This chapter introduces the concept of modules and libraries in Python, allowing you to leverage pre-written code for various tasks.\",\n      \"topics\": [\n        \"What are modules and libraries?\",\n        \"Importing modules\",\n        \"Using built-in modules\",\n        \"Third-party libraries\"\n      ]\n    },\n    {\n      \"chapter_title\": \"Error Handling\",\n      \"summary\": \"This chapter covers how to handle errors in Python programs, ensuring graceful execution and preventing program crashes.\",\n      \"topics\": [\n        \"Types of errors\",\n        \"Try-except blocks\",\n        \"Raising exceptions\"\n      ]\n    }\n  ]\n}\n```"},
          ],
        },
      ],
    });

    export const generateNotesAiModel = model.startChat({
      generationConfig2,
      
    });

    export const GenerateStudyTypeContentAiModel = model.startChat({
      generationConfig,
      history: [
        {
          role: "user",
          parts: [
            {text: "Generate the flashcard on topic : Flutter Fundamentals,User Interface (UI) Development,Basic App Navigation in JSON format with front back content, Maximum 15"},
          ],
        },
        {
          role: "model",
          parts: [
            {text: "```json\n[\n  {\n    \"front\": \"What is a Widget in Flutter?\",\n    \"back\": \"A Widget is the basic building block of a Flutter UI. Everything you see on the screen is a widget, including layout elements, text, images, and more.  They are immutable and describe the UI.\"\n  },\n  {\n    \"front\": \"Explain the difference between StatelessWidget and StatefulWidget.\",\n    \"back\": \"StatelessWidget: Its UI doesn't change after it's built.  StatefulWidget: Its UI can change based on user interaction or other factors. It manages its own state using State objects.\"\n  },\n  {\n    \"front\": \"Name three common layout widgets in Flutter.\",\n    \"back\": \"Row, Column, and Stack are common layout widgets.  Row arranges children horizontally, Column vertically, and Stack overlays children.\"\n  },\n  {\n    \"front\": \"What is the purpose of a `BuildContext`?\",\n    \"back\": \"BuildContext provides information about the location of a widget within the widget tree. It's used to access the theme, parent widgets, and other contextual information.\"\n  },\n  {\n    \"front\": \"How do you display text in Flutter?\",\n    \"back\": \"Use the `Text` widget.  You can style it with properties like `style`, `textAlign`, `textDirection`, etc.\"\n  },\n  {\n    \"front\": \"How do you navigate to a new screen in Flutter?\",\n    \"back\": \"Use `Navigator.push(context, MaterialPageRoute(builder: (context) => NewScreen()));`  This pushes a new route onto the navigation stack.\"\n  },\n  {\n    \"front\": \"How do you pass data to a new screen during navigation?\",\n    \"back\": \"Pass data via the constructor of the new screen's widget.  You can also use named routes and pass arguments via `RouteSettings`.\"\n  },\n  {\n    \"front\": \"What is a `MaterialApp` widget?\",\n    \"back\": \"It's the root widget of a Flutter application that provides material design styling and navigation capabilities.\"\n  },\n  {\n    \"front\": \"What is the purpose of the `Scaffold` widget?\",\n    \"back\": \"Provides a basic visual layout structure for a Material Design app including an AppBar, Body, and Drawer.\"\n  },\n  {\n    \"front\": \"How do you handle user input in Flutter?\",\n    \"back\": \"Using widgets like `TextField` and `Checkbox` to capture user input. Then process these inputs within the state of a StatefulWidget.\"\n  },\n  {\n    \"front\": \"What are keys in Flutter widgets?\",\n    \"back\": \"Keys provide a way to uniquely identify widgets, especially when the structure of the widget tree changes dynamically. This helps Flutter manage the UI effectively during rebuilds.\"\n  },\n  {\n    \"front\": \"Explain the concept of a routing table in Flutter.\",\n    \"back\": \"A routing table (often implemented using `MaterialApp`'s `routes` property) maps named routes to widget builders, allowing for easy navigation to specific screens based on route names.\"\n  },\n  {\n    \"front\": \"What is the difference between `push` and `pushReplacementNamed` in navigation?\",\n    \"back\": \"`push` adds a new route to the navigation stack. `pushReplacementNamed` replaces the current route with a new one, removing the previous route from the stack.\"\n  },\n  {\n    \"front\": \"How to pop a route from the navigation stack?\",\n    \"back\": \"Use `Navigator.pop(context);` or `Navigator.pop(context, data);` to pop the current route and optionally return data to the previous screen.\"\n  },\n  {\n    \"front\": \"What's the role of `initState()` in a StatefulWidget?\",\n    \"back\": \"It's a lifecycle method called only once when the StatefulWidget is inserted into the widget tree. It's used for initializing state variables.\"\n  }\n]\n```\n"},
          ],
        },
      ],
    })

   export const GenerateQuizAiModel = model.startChat({
      generationConfig,
      history: [
        {
          role: "user",
          parts: [
            {text: "Generate Quiz on topic : Flutter Fundamentals,User Interface (UI) Development,Basic App Navigation with Question and Options along with correct answer in JSON format"},
          ],
        },
        {
          role: "model",
          parts: [
            {text: "```json\n{\n  \"quizTitle\": \"Flutter Fundamentals, UI Development & Basic Navigation\",\n  \"questions\": [\n    {\n      \"question\": \"What is the fundamental building block of a Flutter UI?\",\n      \"options\": [\"Widget\", \"Layout\", \"View\", \"Component\"],\n      \"answer\": \"Widget\"\n    },\n    {\n      \"question\": \"Which widget is used to arrange children in a column?\",\n      \"options\": [\"Row\", \"Column\", \"Stack\", \"Container\"],\n      \"answer\": \"Column\"\n    },\n    {\n      \"question\": \"What does `StatelessWidget` mean in Flutter?\",\n      \"options\": [\"A widget that changes its state based on user interaction\", \"A widget whose state never changes\", \"A widget that manages its own state\", \"A widget that relies on external state management\"],\n      \"answer\": \"A widget whose state never changes\"\n    },\n    {\n      \"question\": \"Which widget is best suited for creating a scrollable list of items?\",\n      \"options\": [\"ListView\", \"GridView\", \"Column\", \"Row\"],\n      \"answer\": \"ListView\"\n    },\n    {\n      \"question\": \"How do you navigate to a new screen in Flutter?\",\n      \"options\": [\"Using `Navigator.push`\", \"Using `setState`\", \"Using `BuildContext.push`\", \"Using `Navigator.pop`\"],\n      \"answer\": \"Using `Navigator.push`\"\n    },\n    {\n      \"question\": \"What does the `BuildContext` provide?\",\n      \"options\": [\"Access to the application's theme\", \"Information about the widget's position in the widget tree\", \"A way to access shared preferences\", \"A mechanism for handling user input\"],\n      \"answer\": \"Information about the widget's position in the widget tree\"\n    },\n    {\n      \"question\": \"Which widget is commonly used to display an image in Flutter?\",\n      \"options\": [\"Image.asset\", \"Image.network\", \"Icon\", \"Text\"],\n      \"answer\": \"Image.asset\"\n    },\n    {\n      \"question\": \"What is the purpose of a `Key` in Flutter?\",\n      \"options\": [\"To uniquely identify a widget\", \"To manage state changes\", \"To style widgets\", \"To handle user input\"],\n      \"answer\": \"To uniquely identify a widget\"\n    },\n    {\n      \"question\": \"How do you pass data to a new screen during navigation?\",\n      \"options\": [\"Using arguments in `Navigator.push`\", \"Using `setState`\", \"Using global variables\", \"Using shared preferences\"],\n      \"answer\": \"Using arguments in `Navigator.push`\"\n    },\n    {\n      \"question\": \"What is the role of a `Scaffold` widget?\",\n      \"options\": [\"Provides a basic visual layout structure\", \"Manages app state\", \"Handles navigation\", \"Displays images\"],\n      \"answer\": \"Provides a basic visual layout structure\"\n    }\n  ]\n}\n```\n"},
          ],
        },
      ],
    });
  
    // const result = await chatSession.sendMessage("INSERT_INPUT_HERE");
    // console.log(result.response.text());
 