#include <iostream>      // 引入輸入輸出功能（cin、cout）
#include <string>        // 引入字串 string
using namespace std;     // 讓我們不用寫 std::

string compress(const string &s) {   // 定義一個壓縮字串的函式
    string result = "";              // 用來存壓縮完的字串
    int count = 1;                   // 記錄目前連續字元的數量，初始為 1

    for (int i = 1; i <= s.size(); i++) {   // 從第二個字開始掃到最後（i == size 時也會處理）
        
        if (i == s.size() || s[i] != s[i - 1]) {  
            // 如果到字串尾巴，或字跟前一個不同 → 代表一段重複結束

            if (count > 2) {  
                result += to_string(count) + s[i - 1];   
                // 如果重複 > 2：輸出「重複數 + 字母」
            } else {
                result.append(count, s[i - 1]);  
                // 如果重複 <= 2：直接照原樣複製 count 次
            }

            count = 1;  
            // 段落結束，重置重複次數
        }
        else {
            count++;  
            // 如果字跟前一個一樣 → 重複次數 +1
        }
    }

    return result;   // 回傳壓縮好的字串
}

int main() {
    string s;        // 宣告一個字串變數 s
    cin >> s;        // 從使用者輸入字串

    cout << compress(s) << endl;  // 輸出壓縮後的字串
    return 0;       // 程式結束
}