import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { AlertFeature, AlertResponse } from "./interfaces.js";

const NWS_API_BASE = "https://api.weather.gov";
const USER_AGENT = "mcp-weather-tutorial/1.0 (contact@example.com)";
const chartPng = 'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVR4nGNgAAIAAAUAAXpeqz8AAAAASUVORK5CYII=';

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

// Resource: //config
server.registerResource(
  'config', // name
  'config://app', // URI or template
  {
    title: 'Application Config',
    description: 'Application configuration data',
    mimeType: 'text/plain'
  },
  async uri => ({
    contents: [{ uri: uri.href, text: 'log_level=info\nregion=eu-west-1'}]
  })
);

// Resource: //report
server.registerResource(
    'report',
    'report://latest',
    {
        title: 'Latest usage report',
        description: 'Weekly usage summary with a rendered chart',
        mimeType: 'text/markdown'
    },
    async uri => ({
        contents: [
            { uri: uri.href, mimeType: 'text/markdown', text: 'Active installs grew 12% week over week.' },
            { uri: uri.href, mimeType: 'image/png', blob: chartPng }
        ]
    })
);

server.registerResource(
  'user-profile',
  new ResourceTemplate('users://{userId}/profile', { list: undefined }),
  {
    title: 'User Profile',
    description: 'Profile data for one user',
    mimeType: 'application/json'
  },
  async (uri, { userId }) => ({
    contents: [{ uri: uri.href, mimeType: 'application/json', text: JSON.stringify({ userId, plan: 'pro' }) }]
  })
);

server.registerResource(
  'team-roster',
  new ResourceTemplate('teams://{teamId}/roster', {
    list: async () => ({
      resources: [
        { uri: 'teams://core/roster', name: 'Core team roster' },
        { uri: 'teams://growth/roster', name: 'Growth team roster' }
      ]
    })
  }),
  {
    description: 'Members of one team',
    mimeType: 'text/plain'
  },
  async (uri, { teamId }) => ({
    contents: [{ uri: uri.href, text: `Members of team ${teamId}` }]
  })
);

server.registerPrompt(
  'review-code',
  {
      title: 'Code Review',
      description: 'Review code for best practices and potential issues',
      argsSchema: {
        code: z.string().describe('The code to review')
      }
  },
  ({ code }) => ({
      messages: [
          {
              role: 'user' as const,
              content: { type: 'text' as const, text: `Review this code:\n\n${code}` }
          }
      ]
  })
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