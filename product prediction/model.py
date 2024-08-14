import pandas as pd # type: ignore
import numpy as np # type: ignore
from sklearn.model_selection import train_test_split # type: ignore
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix # type: ignore
from sklearn.linear_model import LogisticRegression # type: ignore
from sklearn.preprocessing import LabelEncoder # type: ignore
import pickle
import matplotlib.pyplot as plt # type: ignore
import seaborn as sns # type: ignore

# Load the CSV files using pandas
orders = pd.read_csv('orders.csv')
products = pd.read_csv('products.csv')
users = pd.read_csv('users.csv')

# Merge the orders and products dataframes
orders_products = pd.merge(orders, products, on='Product ID')

# Merge the orders_products and users dataframes
data = pd.merge(orders_products, users, on='User ID')

# Convert categorical variables to numerical variables
le = LabelEncoder()
data['Category'] = le.fit_transform(data['Category'])
data['Username'] = le.fit_transform(data['Username'])

# Define the features (X) and the target variable (y)
X = data[['User ID', 'Product ID', 'Category', 'Price', 'Rating', 'Username']]
y = data['Product Name']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Logistic Regression model
model = LogisticRegression(max_iter=1000, random_state=42)

# Train the model using the training data
model.fit(X_train, y_train)

# Make predictions on the testing data
y_pred = model.predict(X_test)

# Evaluate the model using accuracy score, classification report, and confusion matrix
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy:.2f}')
print('Classification Report:')
print(classification_report(y_test, y_pred))
print('Confusion Matrix:')
print(confusion_matrix(y_test, y_pred))

# Save the linear model to a file
with open('./linear_model.pkl', 'wb') as file:
    pickle.dump(model, file)

# Get the top 10 products by number of orders
top_products = orders_products['Product Name'].value_counts().head(10)

# Create a bar chart
plt.figure(figsize=(10, 6))
plt.bar(top_products.index, top_products.values)
plt.xlabel('Product Name')
plt.ylabel('Number of Orders')
plt.title('Top 10 Products by Number of Orders')
plt.xticks(rotation=90)
plt.show()

# Create a pie chart
plt.figure(figsize=(8, 8))
plt.pie(top_products.values, labels=top_products.index, autopct='%1.1f%%')
plt.title('Top 10 Products by Number of Orders')
plt.show()

# Create a countplot of top 10 products by number of orders
plt.figure(figsize=(10, 6))
sns.countplot(x="Product Name", data=orders_products.head(10))
plt.title("Top 10 Products by Number of Orders")
plt.xlabel("Product Name")
plt.ylabel("Count")
plt.show()

# Create a barplot of average order price by product category
plt.figure(figsize=(10, 6))
sns.barplot(x="Category", y="Price", data=products)
plt.title("Average Order Price by Product Category")
plt.xlabel("Category")
plt.ylabel("Average Price")
plt.show()

# Create a histogram of order prices
plt.figure(figsize=(10, 6))
sns.histplot(orders_products["Price"], kde=True)
plt.title("Histogram of Order Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.show()

# Create a sample temperature dataset
temperature_data = np.random.rand(24, 7) * 100  # 24 hours, 7 days

# Create a heatmap of the temperature data
plt.figure(figsize=(10, 6))
sns.heatmap(temperature_data, annot=True, cmap="coolwarm", square=True, 
            xticklabels=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], 
            yticklabels=[f"{i}:00" for i in range(24)])
plt.title("Temperature Heatmap")
plt.xlabel("Day of the Week")
plt.ylabel("Hour of the Day")
plt.show()

new_data = pd.DataFrame({'User ID': [...], 'Product ID': [...], 'Category': [...], 'Price': [...], 'Rating': [...], 'Username': [...]})
predictions = model.predict(new_data)

