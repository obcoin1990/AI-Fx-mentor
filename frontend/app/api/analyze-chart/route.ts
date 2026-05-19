import { NextRequest, NextResponse } from 'next/server';
import Anthropic from '@anthropic-ai/sdk';
import { supabase } from '@/lib/supabase';

const client = new Anthropic({
  apiKey: process.env.ANTHROPIC_API_KEY,
});

// Type definitions
interface VisionAnalysis {
  trend: string;
  trend_confidence: number;
  support_zones: Array<{ level: number; touches: number }>;
  resistance_zones: Array<{ level: number; touches: number }>;
  patterns_detected: string[];
  swing_highs: number[];
  swing_lows: number[];
  volatility_warning: boolean;
}

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData();
    const imageFile = formData.get('image') as File;
    const pair = (formData.get('pair') as string) || 'EUR/USD';
    const timeframe = (formData.get('timeframe') as string) || '4H';

    if (!imageFile) {
      return NextResponse.json(
        { error: 'No image provided' },
        { status: 400 }
      );
    }

    // Validate image
    const validTypes = ['image/png', 'image/jpeg', 'image/jpg'];
    if (!validTypes.includes(imageFile.type)) {
      return NextResponse.json(
        { error: 'Invalid image format. Must be PNG or JPG' },
        { status: 400 }
      );
    }

    if (imageFile.size > 5 * 1024 * 1024) {
      return NextResponse.json(
        { error: 'Image too large. Max 5MB' },
        { status: 400 }
      );
    }

    // Convert to base64
    const buffer = await imageFile.arrayBuffer();
    const base64 = Buffer.from(buffer).toString('base64');

    // Call Claude Vision API
    const message = await client.messages.create({
      model: 'claude-3-5-sonnet-20241022',
      max_tokens: 1024,
      messages: [
        {
          role: 'user',
          content: [
            {
              type: 'image',
              source: {
                type: 'base64',
                media_type: imageFile.type as 'image/png' | 'image/jpeg',
                data: base64,
              },
            },
            {
              type: 'text',
              text: `Analyze this forex chart for ${pair} (${timeframe} timeframe).

Extract ONLY these data points as JSON:
- trend: "bullish" | "bearish" | "consolidating"
- trend_confidence: 0-65 (number, capped at 65%)
- support_zones: [{level: price, touches: count}]
- resistance_zones: [{level: price, touches: count}]
- patterns_detected: ["pattern1", "pattern2"]
- swing_highs: [price1, price2]
- swing_lows: [price1, price2]
- volatility_warning: boolean

Return ONLY valid JSON, no markdown, no explanation.`,
            },
          ],
        },
      ],
    });

    // Parse response
    const content = message.content[0];
    if (content.type !== 'text') {
      throw new Error('Unexpected response type from Claude');
    }

    const analysis: VisionAnalysis = JSON.parse(content.text);

    // Cap confidence at 65%
    analysis.trend_confidence = Math.min(analysis.trend_confidence, 65);

    // Log to Supabase
    if (supabase) {
      await supabase.from('audit_logs').insert({
        pair,
        timeframe,
        trend: analysis.trend,
        confidence: analysis.trend_confidence,
        support_zones: analysis.support_zones,
        resistance_zones: analysis.resistance_zones,
        analysis_output: analysis,
      });
    }

    return NextResponse.json(analysis);
  } catch (error) {
    console.error('Vision API error:', error);
    return NextResponse.json(
      { error: 'Failed to analyze chart' },
      { status: 500 }
    );
  }
}
