Shader "VolcicLab/VisionStaticAnnulus"
{
    // Lab stimulus shader: a flat, unlit solid color that renders IN FRONT OF everything.
    // - ZTest Off : never occluded by depth (hands, other stimuli, scene content) — this is
    //               what makes requirement "always visible" true; render queue alone does not.
    // - ZWrite Off: never pollutes the depth buffer for anything else in the scene.
    // - Cull Off  : double-sided. The eye sits on the -Z side of the retino frame, so a
    //               front-culled annulus would face the eye the wrong way.
    // No lighting response of any kind: no lights, no ambient, no GI, no reflections — the
    // fragment is a constant color, which is also why the rendered value is exactly the
    // value we set (useful, since the lab calibrates the headset's inner screens).
    //
    // Owned by: VisionStaticAnnulus (Assets\Scripts\) — see its .cs.md.
    Properties
    {
        _Color ("Stimulus Color", Color) = (0.5, 0.5, 0.5, 1.0)
    }

    SubShader
    {
        Tags
        {
            "RenderType" = "Overlay"
            "Queue" = "Overlay"
            "IgnoreProjector" = "True"
        }

        Pass
        {
            ZTest Off
            ZWrite Off
            Cull Off

            CGPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "UnityCG.cginc"

            uniform float4 _Color;

            struct appdata
            {
                float4 vertex : POSITION;
            };

            struct v2f
            {
                float4 position : SV_POSITION;
            };

            v2f vert(appdata v)
            {
                v2f o;
                o.position = UnityObjectToClipPos(v.vertex);
                return o;
            }

            fixed4 frag(v2f i) : SV_Target
            {
                return _Color;
            }
            ENDCG
        }
    }

    Fallback Off
}
