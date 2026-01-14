#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <algorithm>
#include <string>
#include <numeric>

using namespace std;

struct State {
    vector<int> board;
    int k;
    int zero_pos;
    int g; // cost so far
    int h; // heuristic
};

const std::vector<int> goal = {0,1,2,3,4,5,6,7,8};

// Manhattan distance
int manhattan(const vector<int>& board, int k) {
    int dist = 0;
    int n = k * k;
    for (int i = 0; i < n; i++) {
        int v = board[i];
        if (v == 0) continue;
        int target = v;
        int r1 = i / k, c1 = i % k;
        int r2 = target / k, c2 = target % k;
        dist += abs(r1 - r2) + abs(c1 - c2);
    }
    return dist;
}

// Serialize board to string for hashing
string encode(const vector<int>& b) {
    string s;
    s.resize(b.size() * 3);
    int idx = 0;
    for (int x : b) {
        // 2 digits + space
        s[idx++] = char(x / 10 + '0');
        s[idx++] = char(x % 10 + '0');
        s[idx++] = ',';
    }
    return s;
}

// A* search
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    int k;
    cin >> k;
    int n = k * k;

    vector<int> start(n);
    for (int i = 0; i < n; i++) cin >> start[i];

    auto h0 = manhattan(start, k);

    // Priority queue node: f = g + h
    struct Node {
        int f, g, h;
        vector<int> board;
        int zero_pos;
    };

    struct PQcmp {
        bool operator()(const Node& a, const Node& b) const {
            return a.f > b.f;
        }
    };

    priority_queue<Node, vector<Node>, PQcmp> open;

    Node startNode;
    startNode.board = start;
    startNode.g = 0;
    startNode.h = h0;
    startNode.f = h0;
    startNode.zero_pos = find(start.begin(), start.end(), 0) - start.begin();

    open.push(startNode);

    unordered_map<string, int> best_g;
    unordered_map<string, pair<string,string>> parent;
    // parent[state] = {parent_state, move}

    string startKey = encode(start);
    best_g[startKey] = 0;

    // Move definitions
    vector<pair<int,string>> moves; // (offset, move_name)
    // Move 0 DOWN means blank moves DOWN (swap with tile below)
    // But we output direction blank moves
    // offset = ±1 or ±k
    moves.push_back({-k, "D"});   // blank goes UP => tile goes DOWN
    moves.push_back({+k, "U"});     // blank goes DOWN => tile goes UP
    moves.push_back({-1, "R"});  // blank moves LEFT => tile moves RIGHT
    moves.push_back({+1, "L"});   // blank moves RIGHT => tile moves LEFT

    string goalKey = encode(goal);

    while (!open.empty()) {
        Node cur = open.top();
        open.pop();

        string curKey = encode(cur.board);

        if (curKey == goalKey) {
            // Reconstruct path
            vector<string> path;
            string s = curKey;
            while (s != startKey) {
                auto p = parent[s];
                path.push_back(p.second);
                s = p.first;
            }
            reverse(path.begin(), path.end());
            cout << path.size() << "\n";
            for (auto &m : path) cout << m << "\n";
            return 0;
        }

        int z = cur.zero_pos;
        int zr = z / k, zc = z % k;

        for (auto &mv : moves) {
            int offset = mv.first;
            int nz = z + offset;
            int nr = nz / k, nc = nz % k;

            // Check bounds
            if (nr < 0 || nr >= k || nc < 0 || nc >= k) continue;

            // Disallow left<->right wrap
            if (abs(offset) == 1) {
                if (zr != nr) continue;
            }

            vector<int> nb = cur.board;
            swap(nb[z], nb[nz]);

            string nbKey = encode(nb);
            int ng = cur.g + 1;

            if (best_g.find(nbKey) != best_g.end() && best_g[nbKey] <= ng)
                continue;

            int nh = manhattan(nb, k);
            Node nxt;
            nxt.board = nb;
            nxt.g = ng;
            nxt.h = nh;
            nxt.f = ng + nh;
            nxt.zero_pos = nz;
            open.push(nxt);

            best_g[nbKey] = ng;
            parent[nbKey] = {curKey, mv.second};
        }
    }
    return 0;
}
