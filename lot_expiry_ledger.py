import argparse, json, pathlib, sys

def need(ok, message):
    if not ok: raise ValueError(message)

def integer(x, label, minimum=None):
    need(type(x) is int and abs(x) <= 10**15, label + " must be a bounded integer")
    need(minimum is None or x >= minimum, label + " below minimum")
    return x

def ident(x):
    need(isinstance(x,str) and 0 < len(x) <= 128, "expected nonempty identifier <=128 characters")
    return x

def fields(x, required, optional=()):
    need(type(x) is dict and set(required)<=set(x)<=set(required)|set(optional), "invalid object fields")

def pairs(items):
    out={}
    for k,v in items:
        need(k not in out, "duplicate JSON key")
        out[k]=v
    return out

def load(path):
    with pathlib.Path(path).open('rb') as handle: raw=handle.read(1048577)
    need(len(raw)<=1048576,"input exceeds 1 MiB")
    def bad(x): raise ValueError("nonfinite JSON number")
    return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=bad)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input',help='UTF-8 JSON input; read only')
    args=parser.parse_args()
    try:
        result=analyze(load(args.input))
        print(json.dumps(result,ensure_ascii=True,indent=2,allow_nan=False))
        return 1 if result.get('findings') else 0
    except (ValueError,OSError,RecursionError,OverflowError) as exc:
        print(str(exc),file=sys.stderr);return 2

def analyze(data):
    fields(data,['events']);need(type(data['events']) is list and len(data['events'])<=5000,'events must be a list <=5000')
    lots={};seen=set();day=None;received=issued=disposed=0;allocations=[];findings=[]
    for event in data['events']:
        need(type(event) is dict,'event must be an object')
        kind=event.get('kind')
        required={'receive':['sku','lot','quantity','expires'],'issue':['sku','quantity'],'dispose':['lot','quantity']}
        need(kind in required,'unsupported event kind')
        fields(event,['kind','id','day']+required[kind])
        eid=ident(event['id']);need(eid not in seen,'duplicate event id');seen.add(eid)
        now=integer(event['day'],'day');need(day is None or now>=day,'days must be monotonic');day=now
        qty=integer(event['quantity'],'quantity',1)
        if kind=='receive':
            lot=ident(event['lot']);need(lot not in lots,'lot IDs cannot be reused')
            lots[lot]={'lot':lot,'sku':ident(event['sku']),'expires':integer(event['expires'],'expires'),'quantity':qty};received+=qty
        elif kind=='dispose':
            lot=ident(event['lot']);need(lot in lots,'unknown lot')
            need(qty<=lots[lot]['quantity'],'disposal exceeds stock')
            lots[lot]['quantity']-=qty;disposed+=qty
        else:
            sku=ident(event['sku'])
            eligible=sorted((v for v in lots.values() if v['sku']==sku and v['expires']>day and v['quantity']),key=lambda v:(v['expires'],v['lot']))
            available=sum(v['quantity'] for v in eligible)
            if available<qty:
                findings.append({'event':eid,'kind':'stockout','requested':qty,'eligible':available,'allocated':0});continue
            remain=qty
            for v in eligible:
                take=min(remain,v['quantity'])
                if take:allocations.append({'event':eid,'lot':v['lot'],'quantity':take});v['quantity']-=take;remain-=take
                if not remain:break
            issued+=qty
    remaining=sum(v['quantity'] for v in lots.values())
    need(received==issued+disposed+remaining,'internal conservation failure')
    return {'as_of_day':day,'allocations':allocations,'findings':findings,
            'lots':[dict(lots[k],expired=lots[k]['expires']<=day) for k in sorted(lots)],
            'totals':{'received':received,'issued':issued,'disposed':disposed,'remaining':remaining},
            'policy':'whole units; expires > issue day; earliest expiry then lot ID; all-or-nothing stockouts'}

if __name__=='__main__':sys.exit(main())
