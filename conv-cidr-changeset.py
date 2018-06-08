#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import sys
import pprint
from netaddr import *
from sh import aws


def _get_curr_ipset(ipset_id):
    j = json.loads(
        aws(
            "waf",
            "get-ip-set",
            "--ip-set-id",
            ipset_id,
            "--output",
            "json"
        ).stdout
    )
    return [c['Value'] for c in j['IPSet']['IPSetDescriptors']]


def _get_new_ipset(j):
    newl = []
    for l in j['IPSet']['IPSetDescriptors']:
        ip = IPNetwork(l['Value'])
        if not (ip.prefixlen % 8):
            newl.append("%s" % ip.cidr)
        else:
            bit = (ip.prefixlen / 8 + 1) * 8
            for s_ip in ip.subnet(bit):
                newl.append("%s" % (s_ip))

    return newl


def _get_diff(curr, newl):
    return (
        list(set(curr) - set(newl)),
        list(set(newl) - set(curr))
        )


def main():

    diff_only = False
    if len(sys.argv) > 1 and sys.argv[1] in ("-d", "--diff"):
        diff_only = True

    src = json.load(sys.stdin, encoding='utf-8')
    # get current ipset
    newl = _get_new_ipset(src)
    curr = _get_curr_ipset(src['IPSet']['IPSetId'])
    (del_list, add_list) = _get_diff(curr, newl)

    if diff_only:
        print("Append:")
        pprint.pprint(add_list)
        print("Revoke:")
        pprint.pprint(del_list)
        exit(0)

    token = aws(
        "waf",
        "get-change-token",
        "--output",
        "text"
        ).stdout

    ipset_list = {
        "IPSetId": src['IPSet']['IPSetId'],
        "ChangeToken": token.rstrip(),
        'Updates': []
        }

    for l in del_list:
        ipset_list['Updates'].append(
            {
                "Action": "DELETE",
                "IPSetDescriptor": {
                    "Type": "IPV4",
                    "Value": "%s" % l
                    }
            })

    for l in add_list:
        ipset_list['Updates'].append(
            {
                "Action": "INSERT",
                "IPSetDescriptor": {
                    "Type": "IPV4",
                    "Value": "%s" % l
                    }
            })

    print(json.dumps(ipset_list, indent=4))

if __name__ == '__main__':
    main()
