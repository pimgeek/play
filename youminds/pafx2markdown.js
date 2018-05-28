const root_box = msg.payload["repository"]["items"][0]["item"][0];
// root_box look like
// ${}/.outline[].${}/.outline[].__recursive__
function getBoxTitle(box){
  ret_val = "[无标题]";
  if (box !== undefined && 
    box["properties"] !== undefined &&
    box["properties"][0] !== undefined &&
    box["properties"][0]["property"] !== undefined) {
    props = box["properties"][0]["property"];
    for (var idx in props) {
      if (typeof(props[idx]["$"]) !== "undefined" &&
        props[idx]["$"]["name"] === "name" &&
        typeof(props[idx]["value"]) !== "undefined") {
        ret_val = props[idx]["value"][0];
      }
    }
  }
  return ret_val;
}
function getBoxDesc(box){
  ret_val = "    [无简介]";
  if (box !== undefined && 
    box["properties"] !== undefined &&
    box["properties"][0] !== undefined &&
    box["properties"][0]["property"] !== undefined) {
    props = box["properties"][0]["property"];
    for (var idx in props) {
      if (typeof(props[idx]["$"]) !== "undefined" &&
        props[idx]["$"]["name"] === "description" &&
        typeof(props[idx]["value"]) !== "undefined") {
        ret_val = "    " + props[idx]["value"][0];
      }
    }
  }
  return ret_val;
}
function getBoxContent(box){
  if (box !== undefined && 
    typeof(box["content"]) !== undefined &&
    box["content"] !== undefined) {
    return box["content"][0]["text"];
  }
  else {
    return "[无笔记]";
  }
}
function getInsideBoxes(box){
  if (box !== undefined &&
    typeof(box["childs"]) !== undefined &&
    typeof(box["childs"]) !== "string" &&
    typeof(box["childs"][0]["item"]) !== undefined) {
    return box["childs"][0]["item"];
  }
  else {
    return undefined;
  }
}

function convBoxToMarkdownByLevel(box, level) {
  var md_array = [];
  sub_md_array = [];
  if (box === undefined) {
    return []; // 边界条件
  }
  else if (level < 0 || level > 5) {
    node.error("level 数值超出范围（小于 6 的正整数）！");
    return [];
  } 
  else {
    md_array.push("# " + getBoxTitle(box));
    md_array.push(getBoxDesc(box) + "\n\n" + getBoxContent(box) + "\n\n----\n");
    const sub_box_array = getInsideBoxes(box);
    if (level === 0 || typeof(sub_box_array) === "undefined") {
      
      sub_md_array = [];
    } 
    else {
      var box_idx;
      for (box_idx in sub_box_array) {
        sub_md_array = sub_md_array.concat(
          convBoxToMarkdownByLevel(sub_box_array[box_idx], level - 1));
      }
    }
    md_array = md_array.concat(sub_md_array.map(
      function (str) { 
        if (str !== undefined && str.startsWith('#')) {
          return "#" + str;
        }
        else {
          return str;
        }
      }));
  }
  return md_array;
}

// msg.payload = JSON.stringify(msg.payload);
msg.payload = convBoxToMarkdownByLevel(root_box, 0).join("\n");
// msg.payload = getInsideBoxes(root_box["outline"][2]["outline"][1]);
// msg.payload = root_box;
return msg;
