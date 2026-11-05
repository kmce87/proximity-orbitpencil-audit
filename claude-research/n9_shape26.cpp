// count h of shape (2,1^6) at n=5 for a rep file (entries y >= 0: rho(y)=1, entries -y-1: rho(y)=-1), agreement > 18.
#include <cstdio>
#include <cstdlib>
int rho[32]; int par(int x){return __builtin_parity(x);}
int main(int c,char**v){ FILE*f=fopen(v[1],"r"); int x; while(fscanf(f,"%d",&x)==1){ if(x<0) rho[-x-1]=-1; else rho[x]=1; } fclose(f);
 long long gt=0,eq=0; int a[6];
 for(int b=1;b<32;b++) for(int sb=-2;sb<=2;sb+=4)
 for(a[0]=1;a[0]<32;a[0]++) for(a[1]=a[0]+1;a[1]<32;a[1]++) for(a[2]=a[1]+1;a[2]<32;a[2]++) for(a[3]=a[2]+1;a[3]<32;a[3]++) for(a[4]=a[3]+1;a[4]<32;a[4]++){
   a[5]=a[0]^a[1]^a[2]^a[3]^a[4]; if(a[5]<=a[4]) continue; bool bad=false; for(int i=0;i<6;i++) if(a[i]==b) bad=true; if(bad) continue;
   for(int sg=0;sg<64;sg++){ int ag=0; bool ok=true; for(int w=0;w<32&&ok;w++){ int s=2+sb*(par(b&w)?-1:1); for(int i=0;i<6;i++) s+=((sg>>i&1)^par(a[i]&w))?-1:1; if(s%4){ok=false;break;} int h=s/4; int p=h+rho[w]; if(p<0){ok=false;break;} if(p>0) ag++; } if(!ok) continue; if(ag>18) gt++; else if(ag==18) eq++; }
 }
 printf("%s shape(2,1^6) gt=%lld eq=%lld\n",v[1],gt,eq); }
