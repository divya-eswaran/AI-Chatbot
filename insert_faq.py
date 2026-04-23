from pymongo import MongoClient

# ------------------ CONNECT DB ------------------
client = MongoClient("mongodb://localhost:27017/")
db = client["chatbot_db"]
collection = db["faqs"]

# ------------------ DATASET ------------------
faqs = [
{"question":"what is ai","answer":"Artificial Intelligence enables machines to perform tasks that require human intelligence such as learning and decision making."},
{"question":"what is machine learning","answer":"Machine Learning is a subset of AI that allows systems to learn from data without explicit programming."},
{"question":"what is deep learning","answer":"Deep Learning uses neural networks with many layers to learn complex patterns from data."},
{"question":"difference between ai and ml","answer":"AI is the broader concept of intelligent machines while ML is a subset focused on learning from data."},

{"question":"what is python","answer":"Python is a high-level programming language known for simplicity and readability."},
{"question":"what is java","answer":"Java is an object-oriented programming language used for building applications."},
{"question":"what is c","answer":"C is a procedural programming language widely used in system programming."},
{"question":"what is c++","answer":"C++ is an extension of C that supports object-oriented programming."},
{"question":"what is javascript","answer":"JavaScript is used to create dynamic and interactive web pages."},
{"question":"difference between c and c++","answer":"C is procedural while C++ supports object-oriented programming."},

{"question":"what is database","answer":"A database is an organized collection of data that can be stored and retrieved."},
{"question":"what is sql","answer":"SQL is used to manage and manipulate relational databases."},
{"question":"what is mongodb","answer":"MongoDB is a NoSQL database that stores data in JSON-like format."},
{"question":"difference between sql and nosql","answer":"SQL databases use tables while NoSQL databases store unstructured data."},

{"question":"what is operating system","answer":"An operating system manages hardware and software resources of a computer."},
{"question":"what is linux","answer":"Linux is an open-source operating system used in servers and development."},
{"question":"what is windows","answer":"Windows is an operating system developed by Microsoft."},

{"question":"what is data structure","answer":"A data structure organizes data for efficient access and modification."},
{"question":"what is array","answer":"An array stores elements in contiguous memory locations."},
{"question":"what is linked list","answer":"A linked list connects elements using pointers."},
{"question":"what is stack","answer":"Stack follows Last In First Out principle."},
{"question":"what is queue","answer":"Queue follows First In First Out principle."},

{"question":"what is algorithm","answer":"An algorithm is a step by step procedure to solve a problem."},
{"question":"what is time complexity","answer":"Time complexity measures execution time of an algorithm."},
{"question":"what is space complexity","answer":"Space complexity measures memory usage of an algorithm."},

{"question":"what is html","answer":"HTML is used to structure web pages."},
{"question":"what is css","answer":"CSS is used to style web pages."},
{"question":"what is javascript used for","answer":"JavaScript is used to make web pages interactive."},

{"question":"what is backend","answer":"Backend handles server logic and database operations."},
{"question":"what is frontend","answer":"Frontend is the user interface of a website."},
{"question":"what is full stack development","answer":"Full stack development includes both frontend and backend."},

{"question":"what is api","answer":"API allows communication between software applications."},
{"question":"what is rest api","answer":"REST API follows REST architecture for communication."},

{"question":"what is cloud computing","answer":"Cloud computing provides computing services over the internet."},
{"question":"what is aws","answer":"AWS is a cloud platform provided by Amazon."},

{"question":"what is cybersecurity","answer":"Cybersecurity protects systems from digital attacks."},
{"question":"what is encryption","answer":"Encryption secures data by converting it into unreadable form."},

{"question":"what is neural network","answer":"Neural network is inspired by the human brain for pattern recognition."},
{"question":"what is nlp","answer":"NLP helps machines understand human language."},

{"question":"what is git","answer":"Git is a version control system."},
{"question":"what is github","answer":"GitHub hosts code repositories online."},

{"question":"what is compiler","answer":"Compiler converts code into machine language."},
{"question":"what is interpreter","answer":"Interpreter executes code line by line."},

{"question":"difference between compiler and interpreter","answer":"Compiler translates whole program while interpreter runs line by line."},

{"question":"what is oops","answer":"Object Oriented Programming is based on classes and objects."},
{"question":"what is encapsulation","answer":"Encapsulation hides data inside a class."},
{"question":"what is inheritance","answer":"Inheritance allows reuse of code."},
{"question":"what is polymorphism","answer":"Polymorphism allows same function to behave differently."},
{"question":"what is abstraction","answer":"Abstraction hides implementation details."},

{"question":"what is pointer","answer":"Pointer stores memory address."},
{"question":"what is recursion","answer":"Recursion is a function calling itself."},
{"question":"what is dynamic programming","answer":"Dynamic programming stores subproblem results."},
{"question":"what is greedy algorithm","answer":"Greedy chooses best option at each step."},

{"question":"what is binary tree","answer":"Binary tree has at most two children per node."},
{"question":"what is bst","answer":"BST stores sorted data."},
{"question":"what is graph","answer":"Graph connects nodes using edges."},
{"question":"what is dfs","answer":"DFS explores deeply."},
{"question":"what is bfs","answer":"BFS explores level by level."},

{"question":"what is normalization","answer":"Normalization reduces redundancy in databases."},
{"question":"what is denormalization","answer":"Denormalization improves read performance."},

{"question":"what is http","answer":"HTTP transfers web data."},
{"question":"what is https","answer":"HTTPS is secure HTTP."},

{"question":"what is docker","answer":"Docker runs apps in containers."},
{"question":"what is container","answer":"Container packages app with dependencies."},

{"question":"what is microservices","answer":"Microservices split app into small services."},
{"question":"what is monolithic","answer":"Monolithic builds app as single unit."},

{"question":"what is agile","answer":"Agile is iterative development method."},
{"question":"what is scrum","answer":"Scrum uses sprints for development."},

{"question":"what is devops","answer":"DevOps combines development and operations."},
{"question":"what is ci cd","answer":"CI CD automates deployment."},

{"question":"what is blockchain","answer":"Blockchain is distributed ledger."},
{"question":"what is cryptocurrency","answer":"Cryptocurrency is digital money."},

{"question":"what is big data","answer":"Big data is large complex data."},
{"question":"what is hadoop","answer":"Hadoop processes big data."},

{"question":"what is data science","answer":"Data science extracts insights from data."},
{"question":"what is data mining","answer":"Data mining finds patterns in data."},

{"question":"what is clustering","answer":"Clustering groups similar data."},
{"question":"what is classification","answer":"Classification assigns categories."},

{"question":"what is regression","answer":"Regression predicts values."},

{"question":"what is overfitting","answer":"Overfitting learns noise."},
{"question":"what is underfitting","answer":"Underfitting is too simple model."},

{"question":"what is flask","answer":"Flask is a Python web framework."},
{"question":"what is django","answer":"Django is a full featured web framework."},

{"question":"what is json","answer":"JSON is data format."},
{"question":"what is xml","answer":"XML stores structured data."},

{"question":"what is thread","answer":"Thread is smallest execution unit."},
{"question":"what is process","answer":"Process is running program."},

{"question":"what is deadlock","answer":"Deadlock is resource waiting issue."},
{"question":"what is paging","answer":"Paging manages memory."},
{"question":"what is segmentation","answer":"Segmentation divides memory."}
]

# ------------------ INSERT ------------------
collection.delete_many({})
collection.insert_many(faqs)

print("✅ FAQs inserted successfully!")