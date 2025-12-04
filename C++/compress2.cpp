#include <iostream>
#include <string>
using namespace std;

int main() {
    string s;
    cin >> s;

    string result = "";
    int count = 1;

    for (int i = 1; i <= s.size(); i++) {
        if (i == s.size() || s[i] != s[i - 1]) {
            // 連續段落結束
            if (count > 2) {
                result += to_string(count) + s[i - 1]; // to_string數字轉字串
            } else {
                result.append(count, s[i - 1]); //兩個以下就按照原本的數量原樣打進去
            }
            count = 1;  
        } 
        else {
            count++;  
        }
    }

    cout << result << endl;
    return 0;
}