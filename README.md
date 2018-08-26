# aws-waf-ipset-conv

# Dependency
- python > 2.7
- aws cli

Via __requirements.txt__
- netaddr
- sh

`direnv` Recomend!

# Getting start
## 0. Install
`pip install -r requirements.txt`

## 1. Create ip-set
If you have already created ip-set, skip this step.

```
$ aws waf get-change-token
{
    "ChangeToken": "xxxxxxxxx-c130-4dbf-839c-yyyyyyyyy"
}

$ aws waf create-ip-set --name hoge-ip --change-token xxxxxxxxx-c130-4dbf-839c-yyyyyyyyy
{
    "IPSet": {
        "IPSetId": "vvvvvvvv-ebef-417c-b788-wwwwwwwwww",
        "Name": "hoge-ip",
        "IPSetDescriptors": []
    },
    "ChangeToken": "xxxxxxxxx-c130-4dbf-839c-yyyyyyyyy"
}

```

## 2. Get `hoge-ip`'s ip-set
```
$ aws waf get-ip-set --ip-set-id vvvvvvvv-ebef-417c-b788-wwwwwwwwww > hoge-ip.json
```

## 3. Edit `hoge-ip.json`
CIDR OK!

```
{
  "IPSet": {
    "IPSetId": "vvvvvvvv-ebef-417c-b788-wwwwwwwwww", 
    "Name": "hoge-ip", 
    "IPSetDescriptors": [
      {
        "Type": "IPV4",
        "Value": "192.168.1.0/28"
      }
    ]
  }
}
```

## 4. Convert `hoge-ip.json` to Classed Subnet

Confirm diff.

```
./conv-cidr-changeset.py -d < hoge-ip.json
Append:
['192.168.1.5/32',
 '192.168.1.8/32',
 '192.168.1.12/32',
 '192.168.1.15/32',
 '192.168.1.7/32',
 '192.168.1.10/32',
 '192.168.1.6/32',
 '192.168.1.1/32',
 '192.168.1.4/32',
 '192.168.1.11/32',
 '192.168.1.13/32',
 '192.168.1.9/32',
 '192.168.1.14/32',
 '192.168.1.2/32',
 '192.168.1.0/32',
 '192.168.1.3/32']
Revoke:
[]
```

To convert.
```
./conv-cidr-changeset.py < hoge-ip.json > conved_hoge-ip.json
```

## 5. Apply
```
aws waf update-ip-set --cli-input-json file://converted_hoge-ip.json
```

# Features
- Convert CIDR to Classed subnet.
- Diff current ip-set with local-json-file.
- Detect INSERT or DELETE.
- /22 -> /24 * 2, /28 -> /32 * 16.
- get-change-token & set it converted-json file.

# With Docker
```
docker-compose run --rm conv-cidr-changeset.py -d < hoge-ip.json

# forgot --rm?
docker-compose down
```

# ToDo
- IPv6
