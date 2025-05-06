import json


def generate_standalone_html():
    # 读取 followers.json 文件
    with open('followers.json', 'r', encoding='utf-8') as f:
        followers = json.load(f)

    # 读取 following.json 文件
    with open('following.json', 'r', encoding='utf-8') as f:
        following = json.load(f)

    # 读取 relationship.json 文件
    with open('relationship.json', 'r', encoding='utf-8') as f:
        relationship = json.load(f)

    html_template = f"""
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub 关注关系网络图</title>
    <script src="https://d3js.org/d3.v7.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
        }}

        #graph {{
            width: 100%;
            height: 100vh;
        }}

        .node {{
            stroke: #fff;
            stroke-width: 1.5px;
        }}

        .link {{
            stroke: #999;
            stroke-opacity: 0.6;
        }}

        .label {{
            font-size: 10px;
            text-anchor: middle;
        }}

        .highlighted {{
            stroke: red;
            stroke-width: 3px;
            stroke-opacity: 1;
        }}
    </style>
</head>

<body>
    <div id="graph"></div>
    <script>
        // 内嵌数据
        const followers = {followers};
        const following = {following};
        const relationship = {relationship};

        function drawGraph() {{
            const nodes = [];
            const links = [];

            const hwfan = {{ id: "hwfan", group: 2 }};
            nodes.push(hwfan);

            followers.forEach(follower => {{
                const node = {{ id: follower, group: 1 }};
                nodes.push(node);
                links.push({{ source: node, target: hwfan }});
            }});

            following.forEach(follow => {{
                const node = {{ id: follow, group: 3 }};
                nodes.push(node);
                links.push({{ source: hwfan, target: node }});
            }});

            Object.entries(relationship).forEach(([user, followingUsers]) => {{
                const sourceNode = nodes.find(node => node.id === user);
                followingUsers.forEach(followingUser => {{
                    const targetNode = nodes.find(node => node.id === followingUser);
                    if (sourceNode && targetNode) {{
                        links.push({{ source: sourceNode, target: targetNode }});
                    }}
                }});
            }});

            const width = window.innerWidth;
            const height = window.innerHeight;

            const svg = d3.select("#graph")
               .append("svg")
               .attr("width", width)
               .attr("height", height);

            // 定义箭头标记
            svg.append("defs").append("marker")
               .attr("id", "arrow")
               .attr("viewBox", "0 -5 10 10")
               .attr("refX", 8)
               .attr("refY", 0)
               .attr("markerWidth", 6)
               .attr("markerHeight", 6)
               .attr("orient", "auto")
               .append("path")
               .attr("d", "M0,-5L10,0L0,5");

            const simulation = d3.forceSimulation(nodes)
               .force("link", d3.forceLink(links).id(d => d.id))
               .force("charge", d3.forceManyBody().strength(-200))
               .force("center", d3.forceCenter(width / 2, height / 2))
               .force("x", d3.forceX(d => {{
                    if (d.group === 1) return width * 0.2;
                    if (d.group === 2) return width * 0.5;
                    if (d.group === 3) return width * 0.8;
                }}).strength(1))
               .force("y", d3.forceY(height / 2).strength(0.1));

            const link = svg.append("g")
               .attr("stroke", "#999")
               .attr("stroke-opacity", 0.6)
               .selectAll("line")
               .data(links)
               .join("line")
               .attr("stroke-width", d => Math.sqrt(d.value));

            const node = svg.append("g")
               .attr("stroke", "#fff")
               .attr("stroke-width", 1.5)
               .selectAll("circle")
               .data(nodes)
               .join("circle")
               .attr("r", 5)
               .attr("fill", d => {{
                    if (d.group === 1) return "blue";
                    if (d.group === 2) return "red";
                    if (d.group === 3) return "green";
                }})
               .on("click", handleNodeClick);

            const label = svg.append("g")
               .attr("class", "label")
               .selectAll("text")
               .data(nodes)
               .join("text")
               .text(d => d.id)
               .attr("dx", 12)
               .attr("dy", ".35em")
               .on("click", handleNodeClick);

            simulation.on("tick", () => {{
                link
                   .attr("x1", d => d.source.x)
                   .attr("y1", d => d.source.y)
                   .attr("x2", d => d.target.x)
                   .attr("y2", d => d.target.y);

                node
                   .attr("cx", d => d.x)
                   .attr("cy", d => d.y);

                label
                   .attr("x", d => d.x)
                   .attr("y", d => d.y);
            }});

            let selectedNodes = [];

            function handleNodeClick(event, d) {{
                selectedNodes.push(d);
                if (selectedNodes.length === 2) {{
                    const [node1, node2] = selectedNodes;
                    // 移除之前高亮的连线
                    svg.selectAll(".highlighted")
                       .classed("highlighted", false)
                       .attr("marker-end", null);

                    const relevantLink = links.find(link =>
                        (link.source.id === node1.id && link.target.id === node2.id) ||
                        (link.source.id === node2.id && link.target.id === node1.id)
                    );

                    if (relevantLink) {{
                        const linkElement = svg.selectAll("line")
                           .filter(l => l === relevantLink);
                        linkElement.classed("highlighted", true);

                        // 添加箭头标记表明方向
                        if (relationship[node1.id] && relationship[node1.id].includes(node2.id)) {{
                            linkElement.attr("marker-end", "url(#arrow)");
                        }} else if (relationship[node2.id] && relationship[node2.id].includes(node1.id)) {{
                            linkElement.attr("marker-end", "url(#arrow)");
                        }}
                    }}

                    selectedNodes = [];
                }}
            }}
        }}

        // 页面加载完成后绘制图形
        window.onload = drawGraph;
    </script>
</body>

</html>
"""
    return html_template


# 示例用法
if __name__ == "__main__":
    # 生成HTML内容
    html_content = generate_standalone_html()

    # 保存到文件
    with open("standalone_follow_graph.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    print("独立HTML文件已生成: standalone_follow_graph.html")