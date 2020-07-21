// inlets and outlets
inlets = 1;
outlets = 4;

var myval=0;

if (jsarguments.length>1)
	myval = jsarguments[1];

function bang()
{
	outlet(0,"myvalue","is",myval);
}

function anything()
{
	var a = arrayfromargs(messagename, arguments);
	var b = JSON.parse(a);
	outlet(0,b.left_elbow_angle / 180.0);
	outlet(1,b.right_elbow_angle/ 180.0);
	outlet(2,b.left_arm_angle/ 180.0);
	outlet(3,b.right_arm_angle/ 180.0);
}