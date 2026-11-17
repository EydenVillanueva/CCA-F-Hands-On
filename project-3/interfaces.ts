export interface AlertFeature {
  properties: {
    event?: string;
    areaDesc?: string;
    headline?: string;
    instructions?: string;
    description?: string;
    severity?: string;
    [key: string]: any;
  };
  [key: string]: any;
}

export interface AlertResponse {
  features: AlertFeature [];
};