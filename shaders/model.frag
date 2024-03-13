#version 460

#extension GL_NV_command_list : enable

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

layout(std140, binding = 0) uniform sceneBuffer
{
  SceneData scene;
};

layout(std140, binding = 1) uniform objectBuffer
{
  ObjectData object;
};

layout(commandBindableNV) uniform;

in Interpolants
{
  vec3 wPos;
  vec3 wNormal;
  vec2 uv;
}
IN;

layout(location = 0, index = 0) out vec4 out_color;

void
main()
{
  vec4 color = texture(object.texColor, IN.uv * object.texScale.xy);

  vec3 light_dir = normalize(scene.wLightPos.xyz - IN.wPos);
  vec3 view_dir  = normalize((-scene.viewMatrix[3].xyz) - IN.wPos);
  vec3 half_dir  = normalize(light_dir - view_dir);
  vec3 normal    = normalize(IN.wNormal);

  float intensity  = max(0, dot(normal, light_dir));
  intensity       += pow(max(0, dot(normal, half_dir)), 8);

  out_color = color * object.color * intensity;
}