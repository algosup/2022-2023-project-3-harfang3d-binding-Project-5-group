#![allow(non_upper_case_globals)]
#![allow(non_camel_case_types)]
#![allow(non_snake_case)]

use std::{os::raw::c_int, ffi::CString};

include!("bindings.rs");

fn main(){
    unsafe {
        HarfangInputInit();
        HarfangWindowSystemInit();
        
	    let width: c_int = 1280;
        let height: c_int = 720;
        let windowTitle = CString::new("Harfang - Basic Loop").unwrap();
        let windowTitleBytes = windowTitle.as_ptr();
	    let window = HarfangRenderInitWithWindowTitleWidthHeightResetFlags(windowTitleBytes, width, height, HarfangGetRFVSync());

        let assetsFolder = CString::new("project_compiled").unwrap();
        let assetsFolderBytes = assetsFolder.as_ptr();
        HarfangAddAssetsFolder(assetsFolderBytes);
    
        // rendering pipeline
        let pipeline = HarfangCreateForwardPipelineWithShadowMapResolutionSpot16bitShadowMap(2048, false);
        let res = HarfangConstructorPipelineResources();

        let scene = HarfangConstructorScene();
        let sceneName = CString::new("scene/scene.scn").unwrap();
        let sceneNameBytes = sceneName.as_ptr();
        HarfangLoadSceneFromAssets(sceneNameBytes, scene, res, HarfangGetForwardPipelineInfo());

        let rootNodeName = CString::new("RootNode (gltf orientation matrix)").unwrap();
        let rootNodeNameBytes = rootNodeName.as_ptr();
        let node = HarfangGetNodeScene(scene, rootNodeNameBytes);

        let cameraName = CString::new("Camera").unwrap();
        let cameraNameBytes = cameraName.as_ptr();
        let camera = HarfangGetNodeScene(scene, cameraNameBytes);

        let mouse = HarfangConstructorMouse();
        let keyboard = HarfangConstructorKeyboard();
                    
        while !HarfangKeyKeyboardState(HarfangReadKeyboard(), GetKey(22)) && HarfangIsWindowOpen(window) {
                             
            HarfangUpdateMouse(mouse);
            HarfangUpdateKeyboard(keyboard);

            let dt = HarfangTickClock();
            
            let cam_pos = HarfangGetPosTransform(HarfangGetTransformNode(camera));
            let cam_rot = HarfangGetRotTransform(HarfangGetTransformNode(camera));
            let cam_speed = 1.0;
            HarfangFpsController(keyboard, mouse, cam_pos, cam_rot, cam_speed, dt);
            HarfangSetPosTransform(HarfangGetTransformNode(camera),cam_pos);
            HarfangSetRotTransform(HarfangGetTransformNode(camera),cam_rot);

            HarfangUpdateScene(scene, dt);

            let views = HarfangConstructorSceneForwardPipelinePassViewId();
            let mut viewId: u16 = 0;
            let viewId_ptr = &mut viewId;
            HarfangSubmitSceneToPipelineWithFovAxisIsHorizontal(viewId_ptr, scene, HarfangConstructorIntRectWithSxSyExEy(0, 0, width, height), true, pipeline, res, views);           

            let v = HarfangGetRotTransform(HarfangGetTransformNode(node));
            HarfangVec3SetY(v, HarfangVec3GetY(v) + 1.0 * HarfangTimeToSecF(dt));
            HarfangSetRotTransform(HarfangGetTransformNode(node), v);
            
            
            HarfangFrame();
            HarfangUpdateWindow(window);
        }


    }
}