#include <iostream>
#include <bits/stdc++.h>

using namespace std;
int main() {
  cout << "Hello World!\n";
  
  //input 1s and 0s from spreadsheet here to turn them into format that can be inputted into the regression program
  string death = {"1	1	1	1	1	1	1	1	1	1	1	1	0	1	0	0	0	0	0	0	0	0	0	0"};
  //copy pasting them onto any search bar is able to make them all in one line so they can fit as a single string
  
  for(int i = 0; i < death.length(); i++){
    if(death[i] == '0' || death[i] == '1'){
      cout << death[i];
      cout << " ";
    }
  }
}
