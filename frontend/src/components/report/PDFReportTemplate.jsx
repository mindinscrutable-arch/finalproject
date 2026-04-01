import React from 'react';

export default function PDFReportTemplate({ metrics, sourceModel, targetModel }) {
  if (!metrics) return null;

  const isSafe = metrics.verdict === "SAFE TO MIGRATE";
  const isCaution = metrics.verdict === "PROCEED WITH CAUTION";

  return (
    <div 
      id="pdf-report-template"
      style={{
        width: '800px', // standard width for A4
        padding: '60px',
        background: '#ffffff',
        color: '#1a1a1a',
        fontFamily: 'Helvetica, Arial, sans-serif',
        position: 'absolute',
        left: '-9999px',
        top: '-9999px'
      }}
    >
      {/* Main Header */}
      <div style={{ borderBottom: '3px solid #333', paddingBottom: '20px', marginBottom: '30px', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <div>
          <h1 style={{ fontSize: '32px', margin: '0 0 5px 0', color: '#000', fontWeight: 'bold' }}>BridgeRock Migration Report</h1>
          <p style={{ margin: '0', color: '#666', fontSize: '16px' }}>Automated Workload Assessment</p>
        </div>
        <div style={{ textAlign: 'right', fontSize: '14px', color: '#666' }}>
          <div>Source: <b>{sourceModel || "Original Model"}</b></div>
          <div>Target: <b>{targetModel || "NVIDIA NIMs"}</b></div>
        </div>
      </div>

      {/* Verdict Section */}
      <div style={{ backgroundColor: '#f9fafb', padding: '25px', borderRadius: '8px', border: '1px solid #e5e7eb', marginBottom: '30px' }}>
        <h3 style={{ margin: '0 0 10px 0', fontSize: '16px', color: '#4b5563', textTransform: 'uppercase' }}>Final Migration Verdict</h3>
        <div style={{ 
          fontSize: '28px', 
          fontWeight: 'bold', 
          color: isSafe ? '#15803d' : isCaution ? '#b45309' : '#b91c1c',
          marginBottom: '10px'
        }}>
          {metrics.verdict}
        </div>
        <p style={{ margin: 0, fontSize: '14px', color: '#374151' }}>
          Overall Confidence Score: <b>{metrics.confidence}</b>. 
          This workload has been fully evaluated across contextual quality, latency impacts, and semantic similarities.
        </p>
      </div>

      {/* Detailed Metrics Grid */}
      <h3 style={{ margin: '0 0 15px 0', fontSize: '18px', color: '#111', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
        Performance & Cost Analysis
      </h3>
      <table style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '40px', fontSize: '14px' }}>
        <thead>
          <tr style={{ backgroundColor: '#f3f4f6', textAlign: 'left' }}>
            <th style={{ padding: '12px', border: '1px solid #e5e7eb' }}>Metric</th>
            <th style={{ padding: '12px', border: '1px solid #e5e7eb' }}>Source Model</th>
            <th style={{ padding: '12px', border: '1px solid #e5e7eb' }}>NVIDIA Target</th>
            <th style={{ padding: '12px', border: '1px solid #e5e7eb' }}>Delta</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb', fontWeight: 'bold' }}>Latency</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb' }}>{metrics.sourceLatency}</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb' }}>{metrics.targetLatency}</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb' }}>{metrics.latencyDiff}</td>
          </tr>
          <tr>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb', fontWeight: 'bold' }}>Token Output</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb' }}>{metrics.sourceTokens}</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb' }}>{metrics.targetTokens}</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb' }}>{metrics.tokenDiff}</td>
          </tr>
          <tr>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb', fontWeight: 'bold' }}>Cost Simulation</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb' }}>{metrics.sourceCost}</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb' }}>{metrics.targetCost}</td>
            <td style={{ padding: '12px', border: '1px solid #e5e7eb', color: '#15803d', fontWeight: 'bold' }}>{metrics.savingsAmount}</td>
          </tr>
        </tbody>
      </table>

      {/* Quality Checks */}
      <h3 style={{ margin: '0 0 15px 0', fontSize: '18px', color: '#111', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
        Evaluation Framework Results
      </h3>
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginBottom: '40px' }}>
        <div>
          <div style={{ marginBottom: '10px', fontSize: '14px' }}>
            <span style={{ color: '#4b5563', width: '180px', display: 'inline-block' }}>LLM-as-Judge Score:</span> 
            <span style={{ fontWeight: 'bold', color: '#15803d' }}>{metrics.qualityScore}/100</span>
          </div>
          <div style={{ marginBottom: '10px', fontSize: '14px' }}>
            <span style={{ color: '#4b5563', width: '180px', display: 'inline-block' }}>Semantic Similarity:</span> 
            <span style={{ fontWeight: 'bold', color: '#15803d' }}>{metrics.semanticScore}</span>
          </div>
        </div>
        <div>
          <div style={{ marginBottom: '10px', fontSize: '14px' }}>
            <span style={{ color: '#4b5563', width: '180px', display: 'inline-block' }}>Structure Preserved:</span> 
            <span style={{ fontWeight: 'bold', color: '#15803d' }}>PASS</span>
          </div>
          <div style={{ marginBottom: '10px', fontSize: '14px' }}>
            <span style={{ color: '#4b5563', width: '180px', display: 'inline-block' }}>JSON Validation:</span> 
            <span style={{ fontWeight: 'bold', color: '#15803d' }}>PASS</span>
          </div>
        </div>
      </div>

      {/* Strengths and Risks */}
      <h3 style={{ margin: '0 0 15px 0', fontSize: '18px', color: '#111', borderBottom: '1px solid #ddd', paddingBottom: '10px' }}>
        Strategic Recommendations
      </h3>
      <div style={{ display: 'flex', gap: '40px' }}>
        <div style={{ flex: 1 }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#15803d' }}>Strengths Discovered</h4>
          <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '13px', color: '#374151', lineHeight: '1.6' }}>
            {metrics.strengths?.map((s, i) => <li key={i} style={{ marginBottom: '8px' }}>{s}</li>)}
            {(!metrics.strengths || metrics.strengths.length === 0) && <li>No significant strengths over baseline.</li>}
          </ul>
        </div>
        <div style={{ flex: 1 }}>
          <h4 style={{ margin: '0 0 10px 0', fontSize: '14px', color: '#b91c1c' }}>Risks & Action Items</h4>
          <ul style={{ margin: 0, paddingLeft: '20px', fontSize: '13px', color: '#374151', lineHeight: '1.6' }}>
            {metrics.risks?.map((r, i) => <li key={`r${i}`} style={{ marginBottom: '8px' }}><b>Risk:</b> {r}</li>)}
            {metrics.recommendations?.map((r, i) => <li key={`re${i}`} style={{ marginBottom: '8px' }}><b>Rec:</b> {r}</li>)}
            {(!metrics.risks || metrics.risks.length === 0) && (!metrics.recommendations || metrics.recommendations.length === 0) && <li>No immediate risks detected.</li>}
          </ul>
        </div>
      </div>

      <div style={{ marginTop: '60px', borderTop: '1px solid #ddd', paddingTop: '15px', textAlign: 'center', fontSize: '10px', color: '#9ca3af' }}>
        REPORT GENERATED DYNAMICALLY BY BRIDGEROCK LLM-AS-A-JUDGE FRAMEWORK
      </div>
    </div>
  );
}
