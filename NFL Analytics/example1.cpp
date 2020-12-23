#include <armadillo>
#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>
using namespace std;
vector<vector<double>> multiply(vector<vector<double>> a, vector<vector<double>> b);

vector<vector<double>> transpose(vector<vector<double>> a);

vector<vector<double>> multiply(vector<vector<double>> a, vector<vector<double>> b) {
    vector<vector<double>> c(a.size(), vector<double>(b[0].size()));
    for (int i = 0; i < a.size() /*nplayers*/; i++) {
        for (int j = 0; j < b[0].size(); j++) {
            double dot = 0;
            for (int k = 0; k < a[0].size(); k++) {
                dot += a[i][k] * b[k][j];
            }
            c[i][j] = dot;
            //cout << "ijc" << i << j << c[i][j] << endl;
        }
    }
    return c;
}

vector<vector<double>> transpose(vector<vector<double>> a) {
    vector<vector<double>> b(a[0].size(), vector<double>(a.size()));
    for (int i = 0; i < a.size(); i++) {
        for (int j = 0; j < a[i].size(); j++) {
            b[j][i] = a[i][j];
        }
    }
    return b;
}

double determinant(vector<vector<double>> a) {
    double b;
    if (a.size() != a[0].size()) {
        b = 360.4209001;
        return b;
    }
    if (a.size() == 1) {
        b = a[0][0];
        return b;
    }
    for (int i = 0; i < a.size(); i++) {
        vector<vector<double>> c(a.size() - 1, vector<double>(a.size() - 1));
        int row = 0;
        for (int j = 0; j < a.size(); j++) {
            if (i != j) {
                for (int k = 1; k < a.size(); k++) {
                    c[row][k - 1] = a[j][k];
                }
                row++;
            }
        }
        if (i % 2 == 0) {
            b += a[i][0] * determinant(c);
        }
        else {
            b -= a[i][0] * determinant(c);
        }
    }
    return b;
}

vector<vector<double>> cofactor(vector<vector<double>> a) {
    vector<vector<double>> b(a.size(), vector<double>(a.size()));
    for (int i = 0; i < a.size(); i++) {
        for (int j = 0; j < a.size(); j++) {
            vector<vector<double>> c(a.size() - 1, vector<double>(a.size() - 1));
            int row = 0;
            int col = 0;
            for (int l = 0; l < a.size(); l++) {
                for (int k = 0; k < a.size(); k++) {
                    if (i != l && j != k) {
                        //cout << "ijlk" << i << j << l << k << endl;
                        //cout << a[l][k] << endl;
                        //cout << 1 << endl;
                        c[row][col] = a[l][k];
                        //cout << c[row][col];
                        //cout << "rowcol" << row << col << endl;
                        col++;
                        if (col == a.size() - 1) {
                            row++;
                        }
                    }
                }
                col = 0;
            }
            /*for(int w = 0; w < c.size(); w++){
              for(int v = 0; v < c.size(); v++){
                cout << c[w][v] << " ";
              }
              cout << '\n' ;
            }*/
            if ((i + j) % 2 == 0) {
                b[i][j] = determinant(c);
            }
            else {
                b[i][j] = -1 * determinant(c);
            }
        }
    }
    return b;
}

vector<vector<double>> adjoint(vector<vector<double>> a) {
    vector<vector<double>> b(a.size(), vector<double>(a.size()));
    b = cofactor(a);
    b = transpose(b);
    return b;
}

vector<vector<double>> inverse(vector<vector<double>> a) {
    vector<vector<double>> b(a.size(), vector<double>(a.size()));
    b = adjoint(a);
    double det = determinant(a);
    for (int i = 0; i < a.size(); i++) {
        for (int j = 0; j < a.size(); j++) {
            b[i][j] /= det;
        }
    }
    return b;
}


int main() {

    /*vector<vector<double>> a = {{1,4,5},{7,-6,0},{3,3,8}};
    vector<vector<double>> b =  inverse(a);
    for(int i = 0; i < b.size(); i++){
      for(int j = 0; j < b.size(); j++){
        cout << b[i][j] << " ";
      }
      cout << '\n' ;
    }*/

    int nplayers;
    int ngames;
    std::cout << "How many players?" << endl;
    std::cin >> nplayers;
    std::cout << "How many games?" << endl;
    std::cin >> ngames;
    vector<vector<double>> players(nplayers, vector<double>(ngames));
    vector<double> guesses(nplayers);
    vector<double> wowy(nplayers);
    vector<double> ypp(ngames);

    std::cout << "Type in YPP" << endl;
    for (int i = 0; i < ngames; i++) {
        std::cin >> ypp[i];
    }

    std::cout << "Type 1 for each game the player played in and 0 otherwise, continue after each player" << endl;

    for (int i = 0; i < nplayers; i++) {
        for (int j = 0; j < ngames; j++) {
            cin >> players[i][j];
        }
    }
    /* use the following for Visual Studio*/

    /*for (int i = 0; i < nplayers; i++) {
        std::cin >> players[i][0];
        for (int j = ngames - 1; j > 0; j--) {
            cout << int(players[i][0]) << endl;
            players[i][j] = int(players[i][0]) % 10;
            players[i][0] = int(players[i][0])/10;
        }
    }
 
    cout << "players" << endl;
    for (int i = 0; i < nplayers; i++) {
        for (int j = 0; j < ngames; j++) {
            cout << players[i][j];
        }
        cout << '\n';
    }*/
    /*cout << "ypp" << endl;
    for (int i = 0; i < ngames; i++) {
        cout << ypp[i] << endl;
    }*/

    /*vector<double> yppaverages(ngames);
    for(int i = 0; i < ngames; i++){
      yppaverages[i] = 0;
      int count = 0;
      for(int j = 0; j < nplayers; j++){
        if(players[i][j] == 1){
          count ++;
        }
      }
      if(count != 0){
        yppaverages[i] = ypp[i] / count;
      }
    }

    for(int i = 0; i < nplayers; i++){
      guesses[i] = 0;
      int count = 0;
      for(int j = 0; j < ngames; j++){
        if (players[i][j] == 1){
          guesses[i] += yppaverages[j];
          count ++;
        }
      }
      if(count != 0){
        guesses[i] /= count;
      }
    }*/

    vector<vector<vector<double>>> pgroup(ngames, vector<vector<double>>(nplayers, vector<double>(ngames-1)));
    for (int i = 0; i < ngames; i++) {
        for (int j = 0; j < nplayers; j++) {
            int gnum = 0;
            for (int k = 0; k < ngames; k++) {
                if (i != k) {
                    //cout << "ijk " << i << " " << j << " "<< k << endl;
                    pgroup[i][j][gnum] = players[j][k];
                    gnum++;
                }
            }
        }
    }

    int mode = 999;
    while (mode != 0) {
        std::cout << "Type 1 for regular regression, 2 for averaged regression, 3 for least squares regression, and 0 to end" << endl;
        cin >> mode;
        switch (mode) {
            case 1:{
                vector<vector<double>> playersT = transpose(players);
                //cout << 1 << endl;
                vector<vector<double>> toBeInverted = multiply(players, playersT);
                //cout << 2 << endl;
                using namespace arma;
                mat hype(toBeInverted.size(), toBeInverted.size());
                for (int i = 0; i < toBeInverted.size(); i++) {
                    for (int j = 0; j < toBeInverted.size(); j++) {
                        hype(i, j) = toBeInverted[i][j];
                    }
                }
                mat please;
                mat hype2 = mat(playersT.size(), playersT[0].size());
                if (inv(please, hype)) {
                    please = mat(toBeInverted.size(), toBeInverted.size());
                    please = inv(hype);

                }
                else {
                    for (int i = 0; i < playersT.size(); i++) {
                        for (int j = 0; j < playersT[0].size(); j++) {
                            hype2(i, j) = playersT[i][j];
                        }
                    }
                    please = mat(playersT[0].size(), playersT.size());
                    std::cout << "check1" << endl;
                    please = pinv(hype2);
                    std::cout << "check2" << endl;
                }
                /*for (int i = 0; i < toBeInverted.size(); i++) {
                    for (int j = 0; j < toBeInverted.size(); j++) {
                            toBeInverted[i][j] = please(i, j);
                    }
                }*/
                mat yppt(ypp.size(), 1);
                for (int i = 0; i < ypp.size(); i++) {
                    yppt(i, 0) = ypp[i];
                }


                mat gmatrix(playersT[0].size(), 1);
                gmatrix = please * yppt;

                std::cout << "YPP for each player" << endl;
                for (int i = 0; i < nplayers; i++) {
                    std::cout << gmatrix(i, 0) << endl;
                    wowy[i] = gmatrix(i, 0);
                }
                std::cout << "TADAHHH" << endl;
                break;
            }

            case 2: {
                using namespace arma;
                mat g2matrix(players.size(), 1);
                g2matrix *= 0;

                for (int i = 0; i < ngames; i++) {

                    players = pgroup[i];

                    vector<vector<double>> playersT = transpose(players);
                    //cout << 1 << endl;
                    vector<vector<double>> toBeInverted = multiply(players, playersT);
                    //cout << 2 << endl;
                    using namespace arma;
                    mat hype(toBeInverted.size(), toBeInverted.size());
                    for (int i = 0; i < toBeInverted.size(); i++) {
                        for (int j = 0; j < toBeInverted.size(); j++) {
                            hype(i, j) = toBeInverted[i][j];
                        }
                    }
                    mat please;
                    mat hype2 = mat(playersT.size(), playersT[0].size());
                    if (inv(please, hype)) {
                        please = mat(toBeInverted.size(), toBeInverted.size());
                        please = inv(hype);

                    }
                    else {
                        for (int i = 0; i < playersT.size(); i++) {
                            for (int j = 0; j < playersT[0].size(); j++) {
                                hype2(i, j) = playersT[i][j];
                            }
                        }
                        please = mat(playersT[0].size(), playersT.size());
                        std::cout << "check1" << endl;
                        please = pinv(hype2);
                        std::cout << "check2" << endl;
                    }
                    mat yppt(ypp.size() - 1, 1);
                    int gnum = 0;
                    for (int j = 0; j < ypp.size(); j++) {
                        if (j != i) {
                            yppt(gnum, 0) = ypp[j];
                            gnum++;
                        }
                    }

                    g2matrix += please * yppt;

                }
                g2matrix /= ngames;

                std::cout << "Average YPP for each player" << endl;
                for (int i = 0; i < nplayers; i++) {
                    std::cout << g2matrix(i, 0) << endl;
                }
                std::cout << "TADAHHH" << endl;
                break;
            }
            case 3: {
                //std::cout << "Enter the weights one by one, as a matrix" << endl;
                using namespace arma;
                vector<vector<double>> weights(ngames, vector<double> (ngames));
                for (int i = 0; i < players[0].size(); i++) {
                    for (int j = 0; j < players[0].size(); j++) {
                        if (i == j) {
                            double t;
                            std::cin >> t;
                            weights[i][j] = 1 / (t * t);
                        }
                        else {
                            weights[i][j] = 0;
                        }
                    }
                }

                vector<vector<double>> wplayers(nplayers, vector<double>(ngames));
                wplayers = multiply(players, weights);


                vector<vector<double>> playersT = transpose(wplayers);
                //cout << 1 << endl;
                vector<vector<double>> toBeInverted = multiply(wplayers, playersT);
                //cout << 2 << endl;
                mat hype(toBeInverted.size(), toBeInverted.size());
                for (int i = 0; i < toBeInverted.size(); i++) {
                    for (int j = 0; j < toBeInverted.size(); j++) {
                        hype(i, j) = toBeInverted[i][j];
                    }
                }
                mat please;
                mat hype2 = mat(playersT.size(), playersT[0].size());
                if (inv(please, hype)) {
                    please = mat(toBeInverted.size(), toBeInverted.size());
                    please = inv(hype);

                }
                else {
                    for (int i = 0; i < playersT.size(); i++) {
                        for (int j = 0; j < playersT[0].size(); j++) {
                            hype2(i, j) = playersT[i][j];
                        }
                    }
                    please = mat(playersT[0].size(), playersT.size());
                    std::cout << "check1" << endl;
                    please = pinv(hype2);
                    std::cout << "check2" << endl;
                }
                /*for (int i = 0; i < toBeInverted.size(); i++) {
                    for (int j = 0; j < toBeInverted.size(); j++) {
                            toBeInverted[i][j] = please(i, j);
                    }
                }*/
                mat yppt(ypp.size(), 1);
                for (int i = 0; i < ypp.size(); i++) {
                    yppt(i, 0) = ypp[i];
                }


                mat gmatrix(playersT[0].size(), 1);
                gmatrix = please * yppt;

                std::cout << "YPP for each player" << endl;
                for (int i = 0; i < nplayers; i++) {
                    std::cout << gmatrix(i, 0) << endl;
                    wowy[i] = gmatrix(i, 0);
                }
                std::cout << "TADAHHH" << endl;
                break;
            }
            default: {
                break;
            }
        }

    }
}
