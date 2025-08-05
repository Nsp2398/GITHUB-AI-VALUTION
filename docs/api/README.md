# UCaaS Valuation API Documentation

## Base URL
`http://localhost:5000/api`

## Authentication
Currently, the API doesn't require authentication. This should be implemented for production use.

## Endpoints

### Valuation Calculations

#### Calculate DCF Valuation
```http
POST /valuations/dcf
```

**Request Body:**
```json
{
  "revenue": number,
  "growth_rate": number,
  "ebitda_margin": number,
  "tax_rate": number,
  "discount_rate": number,
  "terminal_growth_rate": number,
  "projection_years": number
}
```

**Response:**
```json
{
  "enterprise_value": number,
  "projected_cash_flows": number[],
  "terminal_value": number
}
```

#### Calculate UCaaS Metrics
```http
POST /metrics/ucaas
```

**Request Body:**
```json
{
  "mrr": number,
  "customers": number,
  "churn_rate": number,
  "cac": number,
  "expansion_revenue": number,
  "contraction_revenue": number
}
```

**Response:**
```json
{
  "arr": number,
  "arpu": number,
  "ltv": number,
  "net_revenue_retention": number,
  "rule_of_40": number
}
```

### File Operations

#### Upload File
```http
POST /files/upload
```

**Request:**
- Content-Type: multipart/form-data
- Body: file (supported types: doc, docx, pdf, xls, xlsx, png, jpg, jpeg)

**Response:**
```json
{
  "filename": string,
  "original_filename": string,
  "file_type": string,
  "file_size": number,
  "processed_data": object
}
```

#### Generate Report
```http
POST /reports/generate-report
```

**Request Body:**
```json
{
  "company_info": {
    "name": string,
    "arr": number
  },
  "valuation_data": {
    "growth_rate": number,
    "gross_margin": number,
    "net_revenue_retention": number
  },
  "market_data": object,
  "peer_comparison": array
}
```

**Response:**
- Content-Type: application/vnd.openxmlformats-officedocument.wordprocessingml.document
- File download response

## Error Handling

All endpoints follow this error response format:
```json
{
  "error": string,
  "details": object (optional)
}
```

Common HTTP status codes:
- 200: Success
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

## Rate Limiting
Currently not implemented. Should be added for production use.

## Development Notes

1. All numeric values should be sent as numbers, not strings
2. Dates should be in ISO 8601 format
3. File uploads are limited to 10MB
4. Response times may vary for report generation
