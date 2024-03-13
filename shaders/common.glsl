struct SceneData
{
  mat4 viewProjMatrix;
  mat4 viewProjMatrixI;
  mat4 viewMatrix;
  mat4 viewMatrixI;
  mat4 viewMatrixIT;

  vec4 wLightPos;

  uvec2 viewport;
  float shrinkFactor;
  float time;
};

struct ObjectData
{
  mat4      worldMatrix;
  mat4      worldMatrixIT;
  vec4      color;
  vec2      texScale;
  vec2      _pad;
  sampler2D texColor;
};

vec4 temp_var = vec4(1.0);