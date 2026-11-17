import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { AlertFeature, AlertResponse } from "./interfaces.js";

const NWS_API_BASE = "https://api.weather.gov";
const USER_AGENT = "mcp-weather-tutorial/1.0 (contact@example.com)";

const server = new McpServer({
  name: "Weather",
  version: "1.0.0"
});

// Helper genérico para peticiones NWS
async function makeNWSRequest<T>(url: string): Promise<T | null> {
  const headers = { "User-Agent": USER_AGENT, "Accept": "application/geo+json" };

  try {
    const response = await fetch(url, { headers, method: "GET" });

    if (!response.ok) {
      console.error(`HTTP error fetching ${url}: ${response.status} ${response.statusText}`);
      return null;
    }

    return (await response.json()) as T;
  } catch (e) {
    console.error("Fetch failure:", e);
    return null;
  }
}

function formatAlert(feature: AlertFeature): string {
  const { properties } = feature;
  return [
    `Event: ${properties?.event || "unknown"}`,
    `Area: ${properties?.areaDesc || "unknown"}`,
    `Description: ${properties?.description || "No description available"}`,
    `Instructions: ${properties?.instructions || "No specific instructions provided"}`
  ].join("\n");
}

// Tool: getAlerts
server.registerTool(
  "getAlerts",
  {
    description: "Get weather alerts for a US state.",
    inputSchema: z.object({
      state: z.string().length(2).describe("Two-letter US state code (e.g. CA, NY)")
    })
  },
  async ({ state }) => {
    const code = state.toUpperCase();
    const url = `${NWS_API_BASE}/alerts/active?area=${code}`;
    const data = await makeNWSRequest<AlertResponse>(url);

    if (!data || !data.features) {
      return {
        content: [{ type: "text", text: `Unable to fetch alerts for state ${code}.` }],
        isError: true
      };
    }

    if (data.features.length === 0) {
      return {
        content: [{ type: "text", text: `No active alerts for ${code}.` }]
      };
    }

    const alerts = data.features.map(formatAlert);

    return {
      content: [{ type: "text", text: alerts.join("\n\n---\n\n") }]
    };
  }
);

// Tool: getForecast
server.registerTool(
  "getForecast",
  {
    description: "Get weather forecast for a location given latitude and longitude.",
    inputSchema: z.object({
      latitude: z.number().describe("Latitude of the location"),
      longitude: z.number().describe("Longitude of the location")
    })
  },
  async ({ latitude, longitude }) => {
    const pointsUrl = `${NWS_API_BASE}/points/${latitude},${longitude}`;
    const pointsData = await makeNWSRequest<any>(pointsUrl);

    if (!pointsData || !pointsData.properties?.forecast) {
      return {
        content: [{ type: "text", text: "Unable to fetch point metadata for this location." }],
        isError: true
      };
    }

    const forecastUrl = pointsData.properties.forecast;
    const forecastData = await makeNWSRequest<any>(forecastUrl);

    if (!forecastData || !forecastData.properties?.periods) {
      return {
        content: [{ type: "text", text: "Unable to fetch detailed forecast periods." }],
        isError: true
      };
    }

    const periods = forecastData.properties.periods;
    const forecasts = periods.map((p: any) => 
      `${p.name}:\nTemperature: ${p.temperature}°${p.temperatureUnit}\nWind: ${p.windSpeed} ${p.windDirection}\nForecast: ${p.detailedForecast}`
    );

    return {
      content: [{ type: "text", text: forecasts.join("\n\n") }]
    };
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Weather MCP server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error starting server:", error);
  process.exit(1);
});