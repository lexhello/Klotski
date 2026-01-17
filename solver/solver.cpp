#include <iostream>
#include <vector>
#include <queue>
#include <unordered_map>
#include <algorithm>
#include <string>

using namespace std;

// const std::vector<int> goal = {1,2,3,4,5,6,7,8, 0};
const std::vector<int> goal = {1,2,3,4,5,6,7,8, 9, 10, 11, 12, 13, 14, 15, 0};

// Check if two moves are opposites
bool isOpposite(const string& move1, const string& move2) {
    // return false;
    if (move1 == "U" && move2 == "D") return true;
    if (move1 == "D" && move2 == "U") return true;
    if (move1 == "L" && move2 == "R") return true;
    if (move1 == "R" && move2 == "L") return true;
    return false;
}

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

    struct Node {
        int f, g, h;
        vector<int> board;
        int zero_pos;
        string last_move;
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
    startNode.last_move = "";

    open.push(startNode);

    unordered_map<string, int> best_g;
    unordered_map<string, pair<string,string>> parent;

    string startKey = encode(start);
    best_g[startKey] = 0;

    // Move definitions: (offset, direction_name)
    // Direction is where the TILE moves (opposite of where blank moves)
    vector<pair<int,string>> moves;
    moves.push_back({-k, "U"});   // blank goes up => tile above moves down becomes up
    moves.push_back({+k, "D"});   // blank goes down => tile below moves up becomes down
    moves.push_back({-1, "L"});   // blank goes left => tile on left moves right becomes left
    moves.push_back({+1, "R"});   // blank goes right => tile on right moves left becomes right

    string goalKey = encode(goal);

    while (!open.empty()) {
        Node cur = open.top();
        open.pop();

        string curKey = encode(cur.board);

        if (best_g[curKey] < cur.g) continue;

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
            
            // Output format: num_moves, then each move as "row,col,direction"
            cout << path.size() << "\n";
            
            // Replay moves to output tile positions
            vector<int> replay = start;
            int zero = find(replay.begin(), replay.end(), 0) - replay.begin();
            
            for (auto &m : path) {
                int tile_pos = -1;
                int dir_offset = 0;
                
                if (m == "U") dir_offset = -k;
                else if (m == "D") dir_offset = +k;
                else if (m == "L") dir_offset = -1;
                else if (m == "R") dir_offset = +1;
                
                tile_pos = zero + dir_offset;
                int tile_row = tile_pos / k;
                int tile_col = tile_pos % k;

                if (m == "U") m = "D";
                else if (m == "D") m = "U";
                else if (m == "L") m = "R";
                else if (m == "R") m = "L";

                // Output: row,col,direction
                cout << tile_row << "," << tile_col << "," << m << "\n";
                
                // Update state
                swap(replay[zero], replay[tile_pos]);
                zero = tile_pos;
            }
            return 0;
        }

        int z = cur.zero_pos;
        int zr = z / k, zc = z % k;

        for (auto &mv : moves) {

            if (!cur.last_move.empty() && isOpposite(cur.last_move, mv.second))
                continue;

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
            nxt.last_move = mv.second;  // Set the last move
            open.push(nxt);

            best_g[nbKey] = ng;
            parent[nbKey] = {curKey, mv.second};
        }
    }
    
    return 0;
}