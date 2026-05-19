import { NextRequest, NextResponse } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Type definitions
interface TradeScenario {
  direction: 'buy' | 'sell';
  entry: number;
  stop_loss: number;
  take_profit: number;
  risk_reward: number;
  confidence: number;
  rationale: string;
}

interface ReasoningOutput {
  scenarios: TradeScenario[];
  mentor_explanation: string;
  overall_confidence: number;
  unreliable: boolean;
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { analysis } = body;

    if (!analysis) {
      return NextResponse.json(
        { error: 'No analysis provided' },
        { status: 400 }
      );
    }

    // Call Claude Reasoning API
    const message = await client.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      messages: [
        {
          role: 'user',
          content: `Based on this forex chart analysis:
${JSON.stringify(analysis, null, 2)}

Generate 1-2 trade scenarios as JSON with this structure:
{
  "scenarios": [
    {
      "direction": "buy" or "sell",
      "entry": price,
      "stop_loss": price,
      "take_profit": price,
      "risk_reward": ratio,
      "confidence": 0-65,
      "rationale": "explanation"
    }
  ],
  "mentor_explanation": "3-5 sentence educational explanation",
  "overall_confidence": 0-65,
  "unreliable": false
}

Rules:
- Cap ALL confidence at 65%
- Entry must be visible on chart
- Stop-loss must be below support (for buy) or above resistance (for sell)
- Take-profit must be above entry (for buy) or below entry (for sell)
- Risk-reward = (TP-Entry)/(Entry-SL) for buy, (Entry-TP)/(SL-Entry) for sell
- Mentor tone: educational, no financial advice ("should buy/sell" forbidden)
- If confidence < 50%, set unreliable: true
- Return ONLY valid JSON`,
        },
      ],
    });

    // Parse response
    const content = message.content[0];
    if (content.type !== 'text') {
      throw new Error('Unexpected response type from Claude');
    }

    const result: ReasoningOutput = JSON.parse(content.text);

    // Validate and cap confidence
    result.overall_confidence = Math.min(result.overall_confidence, 65);
    result.scenarios = result.scenarios.map(s => ({
      ...s,
      confidence: Math.min(s.confidence, 65),
    }));

    // Flag unreliable
    if (result.overall_confidence < 50) {
      result.unreliable = true;
    }

    return NextResponse.json(result);
  } catch (error) {
    console.error('Reasoning API error:', error);
    return NextResponse.json(
      { error: 'Failed to generate scenarios' },
      { status: 500 }
    );
  }
}
