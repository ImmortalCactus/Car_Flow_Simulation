#include <bits/stdc++.h>
#define fi first
#define se second
#define pb push_back
#define mp make_pair
#define all(x) begin(x),end(x)
#define F(i,n) for (int i = 0; i < n; ++i)
#define F1(i,n) for (int i = 1; i <= n; ++i)
#define dbg(x) cerr << #x << " = " << x << endl
#define dbgg(x) cerr << #x << " = " << x << ' '
#define T(x) x[pool]
#define mineq(x,y) { if ((x) > (y)) (x) = (y); }
#define maxeq(x,y) { if ((x) < (y)) (x) = (y); }
#define MEOW { cout << "meowwwww" << '\n'; system("pause"); }
#define int long long
using namespace std;
typedef vector<int> vi;
typedef pair<int, int> pii;

template<typename T>
ostream& operator <<(ostream &s, const vector<T> &c)
{
	s << "[ "; for (auto it : c) s << it << " "; s << "\b]\n";
	return s;
}

template<typename T>
ostream& operator <<(ostream &s, const pair<int, T> &c)
{
	s << "[ "; cout << c.fi << " , " << c.se << " ] ";
	return s;
}

const int maxn = 123456, mod = 10000;

int n;
//string s;

void input()
{
	cin >> n;// >> s;
}

struct tri
{
	int x, y, z;
};

bool coli(pii x, pii y, pii z)
{
	return (x.fi - y.fi) * (x.se - z.se) == (x.fi - z.fi) * (x.se - y.se);
}

double area(pii x, pii y, pii z)
{
	return abs(x.fi * y.se + y.fi * z.se + z.fi * x.se
					 - x.se * y.fi - y.se * z.fi - z.se * x.fi);
}


pii p[maxn];

/*pii gen()
{
    static 
	return 
}*/

bool inside(tri x, pii y)
{
	if (coli(y, p[x.x], p[x.y])) return false;
	if (coli(y, p[x.y], p[x.z])) return false;
	if (coli(y, p[x.z], p[x.x])) return false;
	if (area(y, p[x.x], p[x.y])
	  + area(y, p[x.y], p[x.z])
	  + area(y, p[x.z], p[x.x])
	 <= area(p[x.x], p[x.y], p[x.z]) + 0.001) return true;
	return false;
}

void solve()
{
    mt19937 generator(time(NULL));
    queue<tri> q;
	//F1 (i, 3) p[i] = mp(generator() % mod, generator() % mod);;
	p[1] = mp(0, 0);
    p[2] = mp(mod - 1, 0);
    p[3] = mp(mod - 1, mod - 1);
    p[4] = mp(0, mod - 1);
    vector<tri> t;
	vector<pii> edge;
	t.pb((tri){1, 2, 3});
    t.pb((tri){1, 3, 4});
    q.push(t[0]);
    q.push(t[1]);
	edge.pb(mp(1, 2));
	edge.pb(mp(2, 3));
	edge.pb(mp(3, 1));
  edge.pb(mp(3, 4));
  edge.pb(mp(4, 1));
	//F1 (i, 3) dbg(p[i]);
	F1 (i, n - 4)
	{
		//dbg(i);
		bool in = false;
		do
		{
			//pii cur = mp(generator() % mod, generator() % mod);;
			auto fit = q.front();
			int a = rand() % 10, b = rand() % 10, c = rand() % 10;
			pii cur = mp(p[fit.x].fi * a + p[fit.y].fi * b + p[fit.z].fi * c
			           , p[fit.x].se * a + p[fit.y].se * b + p[fit.z].se * c);
			cur.fi /= a + b + c; cur.se /= a + b + c;
			for (auto x : t) if (inside(x, cur)) in = true;
			//dbgg(cur); dbg(in);
			if (in)
			{
				p[i + 4] = cur;
				for (auto it = t.begin(); it != t.end(); ++it) if (inside(*it, cur))
				{
					auto x = *it;
					edge.pb(mp(i + 4, x.x));
					edge.pb(mp(i + 4, x.y));
					edge.pb(mp(i + 4, x.z));
					t.erase(it);
					t.pb((tri){i + 4, x.x, x.y});
					t.pb((tri){i + 4, x.y, x.z});
					t.pb((tri){i + 4, x.z, x.x});
                    q.push((tri){i + 4, x.x, x.y});
                    q.push((tri){i + 4, x.y, x.z});
                    q.push((tri){i + 4, x.z, x.x});
					q.pop();
                    break;
				}
			}
		} while (!in);
	}
    //string sys = "python ./" + s + ' ';
    cout << n << '\n';
	F1 (i, n) cout << p[i].fi << ' ' << p[i].se << '\n';
	cout << edge.size() << '\n';
	for (auto x : edge) cout << x.fi - 1 << ' ' << x.se - 1 << '\n';
}

main()
{
	input();
	solve();
}