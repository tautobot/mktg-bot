#!/usr/bin/env bash
s=$BASH_SOURCE ; s=$(dirname "$s") ; s=$(cd "$s" && pwd) ; SCRIPT_HOME="$s";
a="$SCRIPT_HOME/../.."; ROOT=$(cd "$a" && pwd);

echo "
-------------------------
START: SPONSORED PURCHASE
-------------------------"
$ROOT/testcases/sponsored_purchase/sponsored_purchase.sh
echo "
-----------------------
END: SPONSORED PURCHASE
-----------------------"

echo "
-------------------------
START: FLEP AUTO RENEWALS
-------------------------"
$ROOT/testcases/flep_renewals/flep_renewals.sh
echo "
-----------------------
END: FLEP AUTO RENEWALS
-----------------------"
echo "
-------------------------
START: FLIP AUTO RENEWALS
-------------------------"
$ROOT/testcases/flip_renewals/flip_renewals.sh
echo "
-----------------------
END: FLIP AUTO RENEWALS
-----------------------"
