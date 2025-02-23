// Import D3.js (Make sure to include D3 in your project)
const data = {
    "India": { "Gemini": { "CEO": [50, 70], "Manager": [45, 60] }, "ChatGPT": { "CEO": [52, 68], "Manager": [46, 59] } },
    "USA": { "Gemini": { "CEO": [50, 70], "Manager": [45, 60] }, "ChatGPT": { "CEO": [51, 69], "Manager": [44, 58] } },
    "UK": { "Gemini": { "CEO": [45, 60], "Manager": [40, 50] }, "ChatGPT": { "CEO": [46, 61], "Manager": [41, 52] } },
    "Germany": { "Gemini": { "CEO": [45, 60], "Manager": [40, 50] }, "ChatGPT": { "CEO": [47, 62], "Manager": [42, 51] } },
    "Japan": { "Gemini": { "CEO": [50, 70], "Manager": [45, 60] }, "ChatGPT": { "CEO": [49, 67], "Manager": [44, 59] } },
    "China": { "Gemini": { "CEO": [50, 70], "Manager": [48, 60] }, "ChatGPT": { "CEO": [51, 68], "Manager": [47, 59] } },
    "Brazil": { "Gemini": { "CEO": [48, 65], "Manager": [44, 55] }, "ChatGPT": { "CEO": [49, 66], "Manager": [45, 54] } },
    "South Africa": { "Gemini": { "CEO": [45, 60], "Manager": [40, 50] }, "ChatGPT": { "CEO": [46, 61], "Manager": [41, 51] } },
    "Australia": { "Gemini": { "CEO": [45, 60], "Manager": [40, 50] }, "ChatGPT": { "CEO": [46, 61], "Manager": [41, 52] } },
    "Canada": { "Gemini": { "CEO": [45, 60], "Manager": [40, 50] }, "ChatGPT": { "CEO": [46, 61], "Manager": [41, 52] } }
};

const svgWidth = 900, svgHeight = 600;
const margin = { top: 50, right: 30, bottom: 50, left: 120 };
const width = svgWidth - margin.left - margin.right;
const height = svgHeight - margin.top - margin.bottom;

const svg = d3.select("body")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .append("g")
    .attr("transform", `translate(${margin.left}, ${margin.top})`);

const countries = Object.keys(data);
const models = ["Gemini", "ChatGPT"];
const roles = ["CEO", "Manager"];
const yScale = d3.scaleBand().domain(countries).range([0, height]).padding(0.2);
const xScale = d3.scaleLinear().domain([30, 80]).range([0, width]);
const color = d3.scaleOrdinal().domain(models).range(["steelblue", "green"]);

svg.append("g").call(d3.axisLeft(yScale));
svg.append("g").attr("transform", `translate(0, ${height})`).call(d3.axisBottom(xScale));

countries.forEach((country) => {
    models.forEach((model, j) => {
        roles.forEach((role, i) => {
            const [minAge, maxAge] = data[country][model][role];
            svg.append("rect")
                .attr("x", xScale(minAge))
                .attr("y", yScale(country) + i * (yScale.bandwidth() / 2) + j * 5)
                .attr("width", 0) 
                .attr("height", yScale.bandwidth() / 2 - 5)
                .attr("fill", color(model))
                .transition()
                .duration(2000)
                .attr("width", xScale(maxAge) - xScale(minAge));
        });
    });
});
