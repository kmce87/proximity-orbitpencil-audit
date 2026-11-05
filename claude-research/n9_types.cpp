// N9: abstract patterns of h = 1/2 + (1/4) sum_i eps_i chi_{a_i}, a_i distinct nonzero, sum a_i = 0, integer valued.
// With l_i(v) = a_i.v + b_i, wt = weight of l(v): h = (2 + m - 2 wt)/4.  Integrality fixes parity of wt on the whole coset.
// Up to GL_r the first r chars are the standard basis; the other m - r chars are free but for the last (sum zero).
// Output: for each (m, r) the distinct histograms of h values, as counts of points of F_2^r, keeping those with h >= -1 somewhere
// allowed: x = #(h=-1), y = #(h=2), y3 = #(h=3), no h <= -2.  Flag "open" if y + 2 y3 < 2^r/16 (needed for overlap < N/16).
#include <cstdio>
#include <cstdlib>
#include <map>
#include <set>
#include <vector>
#include <array>
using namespace std;
typedef array<int,8> Hist; // counts for h = -2(or less), -1, 0, 1, 2, 3, 4+, unused
static map<pair<int,int>, map<Hist,long long>> table;
static void eval(int m,int r,const vector<int>&a){
    // offsets b in F_2^m with parity fixed, modulo the image of v -> (a_i.v) (the first r coordinates can be normalised to 0)
    int free=m-r;
    for(int bb=0;bb<(1<<free);bb++){
        int b=bb<<r; // b_i=0 on the basis chars (translate v), free bits on the others
        Hist H; H.fill(0); bool bad=false;
        for(int v=0;v<(1<<r)&&!bad;v++){
            int wt=0; for(int i=0;i<m;i++) wt+=(__builtin_parity(a[i]&v)^((b>>i)&1));
            int num=2+m-2*wt;
            if(num%4){bad=true;break;}
            int h=num/4;
            if(h<=-2) H[0]++; else if(h>=4) H[6]++; else H[h+2]++;
        }
        if(bad) continue;
        table[{m,r}][H]++;
    }
}
static void rec(int m,int r,vector<int>&a,int minv,int left){
    // choose 'left' further chars, increasing, then the last is determined
    if(left==0){
        int s=0; for(int x:a) s^=x;
        if(s==0) return;
        if((int)a.size()!=m-1) return;
        // s must be new and nonzero
        for(int x:a) if(x==s) return;
        a.push_back(s); eval(m,r,a); a.pop_back();
        return;
    }
    for(int x=minv;x<(1<<r);x++){
        if(__builtin_popcount(x)==1) continue; // basis chars are already used
        a.push_back(x); rec(m,r,a,x+1,left-1); a.pop_back();
    }
}
int main(){
    for(int m:{4,6,8,10}){
        for(int r=2;r<=m-1;r++){
            if((1<<r)-1<m) continue;
            if(r>9) continue;
            vector<int> a; for(int i=0;i<r;i++) a.push_back(1<<i);
            int left=m-r-1;
            if(left<0) continue;
            rec(m,r,a,1,left);
            auto &T=table[{m,r}];
            for(auto&kv:T){
                const Hist&H=kv.first; int R=1<<r;
                int x=H[1],y=H[4],y3=H[5];
                bool neg=H[0]>0, big=H[6]>0;
                bool open=(!neg)&&(!big)&&(16*(y+2*y3)<R);
                bool xpos=x>0;
                printf("m=%d r=%d h<=-2:%d h=-1:%d h=0:%d h=1:%d h=2:%d h=3:%d h>=4:%d mult=%lld %s%s\n",m,r,H[0],x,H[2],H[3],y,y3,H[6],kv.second,open?"OPEN":"closed",(open&&!xpos)?" (x=0)":"");
            }
            fflush(stdout);
        }
    }
    return 0;
}
