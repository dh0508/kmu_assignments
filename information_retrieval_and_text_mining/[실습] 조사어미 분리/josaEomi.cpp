/*
20243187 홍동형
정보검색과텍스트마이닝 과제

변경 요약:
1. 제거 대상 부호 리스트에 "?"와 "!"를 새로 포함.
2. 조사/어미 탐색 함수에서 성공 여부를 반환하도록 하여,
   분리 실패 시 메인 루프에서 메시지를 출력하게 함.
*/

#include <bits/stdc++.h>
using namespace std;

// 텍스트 파일에서 조사/어미 목록을 읽어 리스트(vector<string>)로 반환
vector<string> read_list(const string &path) {
    vector<string> result;
    ifstream fin(path);
    string line;
    while (getline(fin, line)) {
        // 공백 및 개행 제거
        line.erase(remove(line.begin(), line.end(), '\r'), line.end());
        line.erase(remove(line.begin(), line.end(), '\n'), line.end());
        if (!line.empty())
            result.push_back(line);
    }
    return result;
}

// 문자열에서 불필요한 기호 제거
string clean_token(string token) {
    vector<string> symbols = {"\n", "\r\n", "\'", "\"", "-", "=", "/", ".", "(", ")", "!", "?"};
    for (auto &s : symbols) {
        size_t pos;
        while ((pos = token.find(s)) != string::npos) {
            token.erase(pos, s.length());
        }
    }
    return token;
}

// 주어진 어절에 조사/어미가 포함되어 있는지 확인 후 분리
bool split_josaeomi(const string &word, const vector<string> &cand_list, const string &tag) {
    bool found = false;
    for (auto &cand : cand_list) {
        // 단어가 cand로 끝나는지 확인
        if (word.size() >= cand.size() &&
            word.compare(word.size() - cand.size(), cand.size(), cand) == 0) {
            string stem = word.substr(0, word.size() - cand.size());
            cout << "\t" << stem << " + " << cand << tag << "\n";
            found = true;
        }
    }
    return found;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 조사와 어미 목록 불러오기
    vector<string> josa = read_list("./josa96.txt");
    cout << "Loaded Josa: ";
    for (auto &j : josa) cout << j << " ";
    cout << "\n";

    vector<string> eomi = read_list("./eomi152.txt");
    cout << "Loaded Eomi: ";
    for (auto &e : eomi) cout << e << " ";
    cout << "\n";

    ifstream fin("./test.txt");
    string line;
    while (getline(fin, line)) {
        if (line.empty() || line.size() < 2) continue;

        line = clean_token(line);

        stringstream ss(line);
        string w;
        while (ss >> w) {
            cout << w << "\n";
            bool has_josa = split_josaeomi(w, josa, "/조사");
            bool has_eomi = split_josaeomi(w, eomi, "/어미");

            if (!(has_josa || has_eomi)) {
                cout << "\t==> 조사/어미 분리 실패\n";
            }
        }
    }

    return 0;
}
