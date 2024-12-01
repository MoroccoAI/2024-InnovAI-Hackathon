<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
   
</head>
<body>

<h1>Moroccan Budget Optimization API</h1>
<p>This API provides two primary functionalities:</p>
<ul>
    <li><strong>Budget Recommendations</strong>: Offers personalized recommendations to help users optimize their spending.</li>
    <li><strong>Receipt Parsing</strong>: Processes scanned receipts to extract itemized data.</li>
</ul>

<h2>Setup Instructions</h2>
<h3>Prerequisites</h3>
<ul>
    <li>Python 3.8+</li>
    <li>Flask Framework</li>
    <li>MongoDB</li>
</ul>

<h3>Installation</h3>
<ol>
    <li>Clone the repository:
        <pre><code>git clone https://github.com/Yassineaur/BudgetOptimization.git
cd BudgetOptimization</code></pre>
    </li>
    <li>Install dependencies:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
    <li>Seed the database with dummy data:
        <pre><code>python seed.py</code></pre>
    </li>
    <li>Start the Flask server:
        <pre><code>python app.py</code></pre>
    </li>
</ol>

<h2>API Endpoints</h2>

<h3>1. Budget Recommendations</h3>
<p><strong>Endpoint:</strong> <code>GET /recommend</code></p>
<p><strong>Description:</strong> Provides budget-saving recommendations based on user purchase history and current offers.</p>

<p><strong>Request Example:</strong></p>
<pre><code>curl -G "http://127.0.0.1:5000/recommend" \
--data-urlencode "user_id=12345" \
--data-urlencode "days=7"</code></pre>

<p><strong>Success Response:</strong></p>
<pre class="success"><code>{
  "status": "success",
  "recommendation": "بالنظر للمشتريات ديالك، هنا بعض النصائح لتوفير الميزانية...\n..."
}</code></pre>

<h3>2. Receipt Parsing</h3>
<p><strong>Endpoint:</strong> <code>POST /receipt</code></p>
<p><strong>Description:</strong> Processes a base64-encoded receipt image and returns structured item data.</p>

<p><strong>Request Example:</strong></p>
<pre><code>curl -X POST http://127.0.0.1:5000/receipt \
-H "Content-Type: application/json" \
-d '{
    "image": "'"$(cat /path/to/receipt_base64.txt)"'"
}'</code></pre>

<p><strong>Success Response:</strong></p>
<pre class="success"><code>{
  "status": "success",
  "data": {
    "currency": "MAD",
    "items": [
      {"category": "dairy", "cost": 0.89, "name": "Fresh Milk", "quantity": 1},
      {"category": "breakfast", "cost": 2.29, "name": "Muesli", "quantity": 1},
      {"category": "sweets", "cost": 0.95, "name": "Dark Chocolate", "quantity": 2}
    ],
    "purchase_date": "Mon, 23 Apr 2012 19:51:00 GMT",
    "receipt_id": "5.08_20120423_195100",
    "total_amount": 5.08,
    "user_id": "12345",
    "user_location": "Casablanca"
  }
}</code></pre>

<p><strong>Error Response:</strong></p>
<pre class="error"><code>{
  "status": "error",
  "message": "Receipt already scanned."
}</code></pre>

<h2>MongoDB Database Initialization</h2>
<p>The <code>seed.py</code> script populates the following collections with dummy data:</p>
<ul>
    <li><strong>products</strong>: List of Moroccan products and their prices.</li>
    <li><strong>offers</strong>: Active offers and discounts.</li>
    <li><strong>purchases</strong>: User purchase history.</li>
    <li><strong>receipts</strong>: Receipt metadata and details.</li>
    <li><strong>users</strong>: User profile data.</li>
</ul>

<h3>Run the Seeder:</h3>
<pre><code>python seed.py</code></pre>

<h2>Notes</h2>
<p>Ensure MongoDB is running locally or on the specified host. All responses are in Arabic where applicable for localization.</p>

<h2>License</h2>
<p>This project is licensed under the MIT License.</p>

</body>
</html>
