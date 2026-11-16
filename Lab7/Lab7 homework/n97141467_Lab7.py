import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

data = np.loadtxt("Bank_Customer.csv", skiprows=1, dtype=str, delimiter=',')

# 1. 去除無意義特徵：customer_id (第 0 欄) 不使用
# 2. 非數值轉數值
country = data[:, 2]
countries = np.unique(country)
country_onehot = (country[:, None] == countries[None, :]).astype(float)
gender_num = (data[:, 3] == "Male").astype(float).reshape(-1, 1)

numeric_idx = [1, 4, 5, 6, 7, 8, 9, 10]
numeric = data[:, numeric_idx].astype(float)
y = data[:, 11].astype(float).reshape(-1, 1)

X = np.hstack([numeric, gender_num, country_onehot])

# 3. 標準化特徵
X_scaled = StandardScaler().fit_transform(X)
pre_data = np.hstack([X_scaled, y])

print("國家編碼順序:", countries)
print("前處理後形狀:", pre_data.shape)

np.savetxt("Bank_Customer_Preprocessed.csv", pre_data, delimiter=",")


from sklearn.linear_model import LogisticRegression
clf = LogisticRegression()

# 4. 切割 Training / Testing (80% / 20%)
x_train, x_test, y_train, y_test = train_test_split(
    pre_data[:, :-1], pre_data[:, -1], test_size=0.2, random_state=42
)
print("x_train:", x_train.shape, "x_test:", x_test.shape)

clf.fit(x_train, y_train)
pred = clf.predict(x_test)

print(str(round(accuracy_score(pred, y_test) * 100, 2)) + "%")
