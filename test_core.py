import copy,unittest
from lot_expiry_ledger import analyze

def receive(i,lot,q,expiry,sku='s',day=0):return dict(kind='receive',id=str(i),day=day,lot=lot,quantity=q,expires=expiry,sku=sku)
def issue(i,q,day=1,sku='s'):return dict(kind='issue',id=str(i),day=day,sku=sku,quantity=q)

class LedgerTests(unittest.TestCase):
    def test_fefo_tie_and_expired_boundary(self):
        r=analyze({'events':[receive(1,'z',2,5),receive(2,'b',2,3),receive(3,'a',2,3),receive(4,'expired',99,1),issue(5,5)]})
        self.assertEqual([(x['lot'],x['quantity']) for x in r['allocations']],[('a',2),('b',2),('z',1)])
        self.assertEqual(r['totals'],dict(received=105,issued=5,disposed=0,remaining=100))
    def test_stockout_is_atomic_and_later_issue_succeeds(self):
        r=analyze({'events':[receive(1,'a',3,5),issue(2,4),issue(3,2)]})
        self.assertEqual(r['findings'][0]['allocated'],0);self.assertEqual(r['allocations'],[dict(event='3',lot='a',quantity=2)])
    def test_disposal_and_sku_isolation(self):
        r=analyze({'events':[receive(1,'a',5,0),receive(2,'b',3,9,'other'),dict(kind='dispose',id='3',day=1,lot='a',quantity=2),issue(4,1)]})
        self.assertEqual(r['totals'],dict(received=8,issued=0,disposed=2,remaining=6));self.assertTrue(r['findings'])
    def test_unit_priority_oracle(self):
        for request in range(1,13):
            es=[receive(i,str(i),i%3+1,i%4+2) for i in range(1,7)];original=copy.deepcopy(es)
            units=sorted((e['expires'],e['lot']) for e in es for _ in range(e['quantity']))
            out=analyze({'events':es+[issue(10,request)]});actual=[a['lot'] for a in out['allocations'] for _ in range(a['quantity'])]
            self.assertEqual(actual,[lot for _,lot in units[:request]]);self.assertEqual(es,original)
    def test_invalid_state(self):
        cases=[[receive(1,'a',True,5)],[receive(1,'a',1,5),receive(2,'a',1,5)],[issue(1,1,3),issue(2,1,2)],[dict(kind='dispose',id='1',day=0,lot='missing',quantity=1)]]
        for es in cases:
            with self.assertRaises(ValueError):analyze({'events':es})

if __name__=='__main__':unittest.main()
