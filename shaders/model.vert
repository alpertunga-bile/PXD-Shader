#version 460

#extension GL_NV_command_list : enable
#extension GL_buffer_reference : require

from common.glsl import SceneData;
from common.glsl import ObjectData;
from common.glsl import temp_var;

layout(std140, binding = 0) uniform sceneBuffer
{
  SceneData scene;
};

layout(std140, binding = 1) uniform objectBuffer
{
  ObjectData object;
};

layout(commandBindableNV) uniform;

in layout(location = 0) vec3 pos;
in layout(location = 1) vec3 normal;
in layout(location = 2) vec2 uv;

in Interpolants
{
  vec3 wPos;
  vec3 wNormal;
  vec2 uv;
}
OUT;

void
main()
{
  vec3 wPos    = (object.worldMatrix * vec4(pos, 1)).xyz;
  vec3 wNormal = mat3(object.worldMatrixIT) * normal;

  gl_Position = scene.viewProjMatrix * vec4(wPos, 1);

  OUT.wPos    = wPos;
  OUT.wNormal = wNormal;
  OUT.uv      = uv;
}