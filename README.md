# Volciclab Programmable Scotoma Reference Project

This is a relatively simple, and stand-alone project for demonstrating a central scotoma with the Meta Quest Pro's eye tracker, so you can use it in your application/experiment with minimal customisation.

The code was made with our local AI-accelerated workflow, and the development-specific files (including the entire Unity documentation tree, session transcripts, and `AGENTS.md`) are not included in this repository. Prying eyes may flag these missing.

## How it works

It uses the face expression API for blink detection and the eye tracker for retino-centric stimulus presentation. It also has the passthrough enabled by default.

It includes all the necessary workarounds and scripts so that it can work stand-alone. See the 'Scripts' directory for details. `Assets/Scripts/<script_name>.cs` is the script, and `Assets/Scripts/<script_name>.cs.md` is the corresponding documentation.

Some of this code is AI generated. This shouldn't be surprising in 2026.

Pinch detection must be done with `OvrHand.GetFingerIsPinching`

## If you start from scratch instead of using this project

This project was built up this way too:

(note that newer versions allow the downloading of new dependencies of build profiles, provided that they are there)

1. Install Unity Hub
2. Install a Unity editor version of whatever is available (ideally LTS)
3. `Asset Store` > `Meta XR Core SDK` > Install
4. `Asset Store` > `Meta XR Interaction SDK Essentials` > Install
5. (for now, ignore whatever `Project Setup Tool` is complaining about)
6. `File` > `Build Profiles` > `Add build Profile` (if you see it) > `Platforms` > `Android` (this can also be `Meta Quest` if the option is there) > `Switch Platform`
7. `Asset Store` > `Unity Registry` > `OpenXR Plugin` > `Install`
8. `Meta XR SDK` > `Project Setup Tool` > `Outstanding Issues` (**Read** and _understand_ these) > `Fix`
9. `Meta XR SDK` > `Project Setup Tool` > `Recommended Items` (**Read** and _understand_ these) > `Fix` _or_ `Mark as Fixed` _or_ `[kebab menu]` > `Ignore` (foveated rendering should stay off!)
10. Close and reopen Unity Editor (see the next subsection if it wants to go to safe mode). Optionally, copy `Unity/Hub/Editor/<your current version>/Documentation` to `Assets`, which will help you, and your AI agent.
11. `Meta XR Feature Set must be enabled in OpenXR Feature Groups to support Meta Quest Features. Do you want to enable it now?` > `Yes`
12. `Meta XR SDK` > `Building Blocks` > `Core` > `Camera Rig` > (Drag to Hierarchy, under the scene)
13. `Meta XR SDK` > `Building Blocks` > `Core` > `Passthrough` > (Drag to Hierarchy, under the scene)
14. `Meta XR SDK` > `Building Blocks` > `Core` > `Hand Tracking` > (Drag to Hierarchy, under the scene)
15. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Camera Rig (Script)` > `User Per Eye Cameras` (untick)
16. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Quest` > `Target Devices` > `Quest Pro` > (tick, and maybe 'VR Glasses' should also be ticked)
17. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Quest Features` > `General` > `Hand Tracking Support` > `Hands Only`
18. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Quest Features` > `General` > `Hand Tracking Frequency` > `Max`
19. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Quest Features` > `General` > `Passthrough Support` > `Required`
20. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Quest Features` > `General` > `Face Tracking Support` > `Required`
21. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Quest Features` > `General` > `Eye Tracking Support` > `Required`
22. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Performance & Quality` > `Local Dimming` > (untick, **this is important**)
23. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Performance & Quality` > `Sharpen Type` > `None`
24. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Tracking` > `Tracking Origin Type` > `Eye Level` (..if you even want to use it with OptiTrack)
25. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Tracking` > `Face Tracking` > `Audio` (untick)
26. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Permission Requests on Startup` > `Eye Tracking` > (tick)
27. `[BuildingBlock] Camera Rig` > (Inspector) > `OVR Manager (Script)` > `Permission Requests on Startup` > `Face Tracking` > (tick)
28. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` (right click) > `Create Empty` > Name it as `GazeContingentGameObject`
29. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` > `GazeContingentGameObject` > (inspector) > `Position` > [x=0, y=0, z=0.5]
30. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` > `GazeContingentGameObject` > (inspector) > Drag `GazeContingentTransform2.cs` under `Add component`
31. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` > `GazeContingentGameObject` (right click) > `Create Empty` > Name it as `Scotoma`
32. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` > `GazeContingentGameObject` > (inspector) > `Add Component` > `OVR Face Expressions`
(you can add a script to this GameObject to create the scotoma, or add any object so that it would be gaze-contingent)
33. Right Click in an empty space in `Hierarchy` > `Create Empty` > Name it as `External Control Scripts`
34. Drag `Assets > Scripts` > `ExternalHandRenderingControl.cs` to  `External Control Scripts` GameObject in scene
35. Drag `Assets > Scripts` > `ExternalPassthroughControl.cs` to  `External Control Scripts` GameObject in scene
36. Drag `Assets > Scripts` > `ExternalEyeTrackerControl.cs` to  `External Control Scripts` GameObject in scene
37. Drag `Assets > Scripts` > `ExternalScotomaDistanceAdjuster.cs` to  `External Control Scripts` GameObject in scene
38. Drag `Assets > Scripts` > `ExternalInterpupillaryDistanceReporter.cs` to `External Control Scripts` GameObject in scene
39. Drag `Assets > Scripts` > `ExternalEyeTrackerAzimuthElevationAdjuster.cs` to `External Control Scripts` GameObject in scene
40. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` (right click) > `Create Empty` > Name it as `HeadContingentGameObject`
41. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` >`HeadContingentGameObject` >  (right click) > `Create Empty` > Name it as `EyeTrackerCalibrator`
42. Drag `Assets > Scripts` > `VisionStaticAnnulus.cs` to `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` >`HeadContingentGameObject` > `EyeTrackerCalibrator`
43. Drag `Assets > Scripts` > `VisionStaticAnnulus.cs` to `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` >`Gaze ContingentGameObject` > `Scotoma`
44. Drag `Assets > Scripts` > `ExternalVisionStaticAnnulusAdjuster.cs` to `External Control Scripts` GameObject in scene
45. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` > `GazeContingentGameObject` > `Scotoma` > (inspector) > `Vision Static Annulus (Script)` > `Render Queue` > 3002
46. `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` >`HeadContingentGameObject` > `EyeTrackerCalibrator` > (inspector) > `Vision Static Annulus (Script)` > `Render Queue` > 3001
47. Drag `Assets > Scripts` > `CrankFrameRateUp.cs` to `[BuildingBlock] Camera Rig` (one-shot at startup: requests the `refreshRate` field — default `90` Hz, the Quest Pro's maximum of its 72/80/90 panel (`0` = device max) — from the runtime, confirms it by read-back, then watches for silent thermal drops; sibling doc `Assets/Scripts/CrankFrameRateUp.cs.md`)
48. Drag `Assets > Scripts` > `NtpTimeSync.cs` to `[BuildingBlock] Camera Rig` (at start it takes `sampleCount` NTP round trips to `ntpServerHost` — default `ae.pool.ntp.org` — and stores the offset between the headset's own system clock and that reference; exposes the corrected UTC clock via `NtpTimeSync.UnixTimeNowInMs()` / `UnixTimeNowInMsString()` so the headset and the lab computers share a **millisecond-precision** time base. Silent fallback: until the first good sample lands, timestamps are the *uncorrected* system clock and `IsSynced` is `false` — nothing blocks. No UDP control port (NTP client to `123`, ephemeral local port), no scene dependencies. Sibling doc `Assets/Scripts/NtpTimeSync.cs.md`)
49. `[BuildingBlock] Camera Rig` > (inspector) > `NTP Time Sync (Script)` > `Ntp Server Host` > (change this to your own NTP server)
50. Drag `Assets > Scripts` > `DataTransmitter.cs` to `[BuildingBlock] Camera Rig`. Decimation control port is `40008`. This is to be used in conjunction with [the Universal Data Sink](https://github.com/ha5dzs/universal-data-sink), so the `Data Sink Ip Address` must be the computer this code is running on.

Make sure that you have the headset connected, debugging enabled, and your computer has permission to do the debugging. Then in `File` > `Build Profiles` > `Run Device`, you should see the ID of the headset. Clicking `Build` creates the apk file to be run on the headset, and `Build And Run` also installs it.

Optional steps:

* If you want to have a tester object at Unity's origin, so you would know where you are with respect to it, then:
  * Right Click in an empty space in `Hierarchy` > `Create Empty` > Name it as `External Control Scripts`
  * Add a mesh as a child (here, it's bundled in `Assets` > `Objects` > `AxisOrientationTester.obj`)
    * If using this object, and `Y` and `Z` is to be swapped, then just set the rotations as X: `-90`, Y: `0`, Z: `180` (this is lab convention)
    * Perhaps scaling (X: `0.002`, Y: `0.02`, Z: `0.02`) might also be a good idea

* If you want to align the coordinate systems (the Unity world ↔ OptiTrack/Motive world), then:
  * **`Assets/Scripts/UnityOptitrackAlignment.cs`** is the script (sibling doc: `UnityOptitrackAlignment.cs.md`). The 2026 Christmas-break predecessor, `universe_relocator.cs`, is kept for reference only — same protocol, same math, tamed failure modes.
  * Attach it to the **`[BuildingBlock] Camera Rig`** (or any ancestor of `CenterEyeAnchor` whose parent is identity — NOT `CenterEyeAnchor` or `GazeContingentGameObject` themselves).
  * It **never auto-aligns** (`requestAlignmentOnStart = false` in the template). The sockets are bound and listening (a listening socket transmits nothing, so the template stays demo-able on an isolated AP); an alignment runs only on an explicit trigger:
    * check **`Request Alignment on Start`** → one alignment run is requested when the app starts (it also works as a live manual trigger if ticked in the Inspector);
    * the port/Inspector/code/recenter triggers from below.
  * **`swapYAndZCoordinates`** is `on` for the lab's convention (OptiTrack/Motive is Z-up, Y-depth, as plotted; Unity is Y-up, Z-depth). Labs streaming standard OptiTrack (Z-depth, Y-up — already Unity order) turn it `off`.
  * The headset's own pose read is noisier than the OptiTrack side, so it is averaged over **`anchorSampleCount`** frames (default `3`; `1` = the original single read) before the correction is applied. Keep it small — nothing guarantees the headset is stationary during the alignment.
  * Set `controlPort` / `rigidBodyID` if your lab differs (defaults: both `5000`).
  * In Motive: a rigid body whose local origin corresponds to `CenterEyeAnchor` (created in the aligned cradle), stable tracking.
  * Then, from the experimenter software / any UDP client:
    * send anything to port `5000` → one alignment run;
    * send `0,0.01,0` → adds that Y-up translation delta (metres) to the running fudge, then aligns — the live "tuning knob" for the visual verification (twin object vs IRL, through the optics gap);
    * send `?` → reads back `OK;<STATE>;<fx,fy,fz>;errMm;errDeg;attempts`.
  * Verify with the **`Origin Tester Object`** (the axis gizmo at Unity's origin, README optional step above): with a good alignment + fudge it should appear to sit exactly on the IRL tracker origin.
  * Optional diagnostic: **`Assets/Scripts/RecenterProbe.cs`** — answers, with evidence, whether *triggering* a tracker recenter works on this project's Eye-Level origin (the alignment script's *detection* hook, `RecenteredPose`, is wired from SDK 207). Throwaway by design; delete the file if unneeded.

* If you want externally tracked rigid bodies in your application
  * `[BuildingBlock] Camera Rig` > `TrackingSpace` > `CenterEyeAnchor` (right click) > `Create Empty` > Name it to personal taste
  * Drag `Assets > Scripts` > `StreamRigidBodyFromOptitrack.cs` to the GameObject you just created
    * You can keep `Use Random Listening Port` on for testing, but in production:
      * Turn `Use Random Listening Port` off
      * Set `Listening Port` statically that matches the convention of the project
  * Add the mesh as the child of the GameObject
    * IMPORTANT THINGS TO CONSIDER:
      * The OptiTrack rigid body's local coordinate system's origin (currently called 'Bone position' née 'Pivot') is streamed:
        * Translation (X-Y-Z) coordinates, switchable 'which axis is up' convention
        * Quaternions (qx, qz, qz, qw), and adapted appropriately depending on the switchable 'which axis is up' convention
      * If you want to have a virtual alterego of the physically tracked object:
        * The origins of the rigid body definition and the mesh **must** correspond
        * This only can be **manually**, **visually** verified by you. It cannot be automated.
      * You probably need to scale *and* rotate this child mesh


## Important files

Every lab script under `Assets/Scripts/` has a sibling Markdown doc.

* `Assets/Scripts/GazeContingentTransform2.*`
This is for the eye tracker.
* `Assets/Scripts/ExternalPassthroughControl.*`
This is for being able to externally control the passthrough over the LAN
* `Assets/Scripts/ExternalHandRenderingControl.*`
This is for showing/hiding the headset's basic hand model within the scene over the network. It's a convenience feature and is not accurate.
* `Assets/Scripts/ExternalEyeTrackerControl.*`
This script is for controlling the eye tracker and the blink detector's sensitivity. Meddle with these variables if the eye tracked object is too jerky in the scene or the eye tracked object slips with eye blinking.
* `Assets/Scripts/ExternalEyeTrackerAzimuthElevationAdjuster.*`
This is also for the eye tracker control, but it is for reading the current gaze with the offsets, and setting the offsets programmatically. This is needed for calibration: you create a stimulus at Az;El, you ask the participant to look at it, get the current Az;El gaze vector returned by this script, calculate the differences, and then you send the difference back as offset. And if you read back the current gaze vector, it should match with the stimulus.
* `Assets/Scripts/ExternalScotomaDistanceAdjuster.*`
This script is for changing the default distance on how much the scotoma and the head-contingent GameObjects are rendered in front of the user. This is for changing the binocular disparity of the renderings, in case the participant complains about double vision of either the stimulus or the scotoma.
* `Assets/Scripts/ExternalInterpupillaryDistanceReporter.*`
The lenses in the Quest Pro are manually adjustable, and the adjustment value is only visible to the user: it is not visible through Casting. So this script reads out the set value, to make sure that it is as per the participant's anatomical measurements. Note that this value only can be queried, and not set, and it only returns a valid value, when the headset is worn, and not when the proximity sensor is disabled in MQDH.
* `Assets/Scripts/VisionStaticAnnulus.*`
This is the annulus renderer script. Can be used for inducing visual deficits and for creating a calibration target for the eye tracker.
* `Assets/Scripts/ExternalVisionStaticAnnulusAdjuster.*`
This is the external control for the two annuli over the LAN: port `40006` drives the gaze-contingent one (the scotoma) and port `40007` drives the head-contingent one (the calibration stimulus) — the toggle, the center (azimuth/elevation), the inner and outer diameters (degrees of visual angle), and the colour; one script, two sockets. The calibration loop that uses them is in the next section, and `eye_tracker_calibration_demo.py` (repo root) runs that whole loop hard-coded, for a live demonstration from another computer (demo-grade, not for production).
* `Assets/Scripts/CrankFrameRateUp.*`
One-shot at startup: requests the `refreshRate` (default 90 Hz — the Quest Pro's maximum of its 72/80/90 panel; `0` = the device maximum) from the runtime, confirms it by read-back, and afterwards watches for silent thermal downgrades (a 90→72 drop is logged the moment it happens). Log markers are `Warning`-level on purpose, so they are visible in Meta Quest Developer Hub under any log-level setting — read the sibling `.cs.md` for the two startup pitfalls this script works around (the `isHmdPresent` session-state timing, and the log-level trap). Attached to the `[BuildingBlock] Camera Rig` (setup step 47). No UDP port, no scene dependencies.
* `Assets/Scripts/NtpTimeSync.*`
Corrected UTC clock for the headset. At start it takes a couple of NTP round trips to `ntpServerHost` (default `ae.pool.ntp.org`) and stores the offset between the headset's own system clock and that reference; every other script then calls `NtpTimeSync.UnixTimeNowInMs()` (or `UnixTimeNowInMsString()`) to get a **millisecond-precision** corrected UTC timestamp so the headset and the lab computers sit in the same time frame (this is what makes precise network / OptiTrack streaming-latency measurement meaningful). `DataTransmitter` (rewritten 2026-11-06) now sources its `TimestampMs` field from `NtpTimeSync.UnixTimeNowInMs()` directly — its old raw-clock `unix_time_now_in_ms()` is gone. Silent fallback: until the first good sample lands, timestamps are the uncorrected system clock (`IsSynced` is `false`) and nothing blocks. No UDP control port by design (a NTP client to `123` with an ephemeral local port), so it consumes no `40000`–`40007` number. Attached to the `[BuildingBlock] Camera Rig` (setup step 48).
* `Assets/Scripts/UnityOptitrackAlignment.*`
This is the **OptiTrack↔Unity world alignment** over the LAN (port `5000`, outside the `40000`–`40007` block): trigger an alignment, add a relative translation fudge (`<x>,<y>,<z>`), or query the state (`?`). The sockets are always bound (listening only — they transmit nothing, so isolated-AP demonstrations are unaffected), but **nothing auto-runs by default** (`requestAlignmentOnStart = false`): an alignment happens only on an explicit trigger. It exposes the original's **`swapYAndZCoordinates`** option (lab convention: OptiTrack Z-up / Y-depth → Unity Y-up / Z-depth; `off` for standard OptiTrack). `universe_relocator.cs` (no sibling doc) is its *superseded* Christmas-break predecessor, kept for reference; `RecenterProbe.cs` (no sibling doc, throwaway by design) is the diagnostic for the tracker-recenter *trigger* question.


## Network communication protocol

As this is a skeleton project, most global variables inside the game engine has to be accessible from the local network, for experimental control. These scripts are loaded to a separate GameObject in Unity, they are not rendered, but they have access to the render loop.

So far, the documented requirements for external access are:

Communication is done via UDP - with the payload of the packets being a plain ASCII string, and the game engine should accept connection from any (`IPAddress.Any`) host. Communication is done in a non-blocking, asynchronous way, with callback functions. There is a Python script available for testing - `PythonUdpBlaster`, which is included in this project. Consults its README on how to use it, if these two lines (`python3 PythonUdpBlaster 192.168.42.125 40002 "0" 0` and `python3 PythonUdpBlaster 192.168.42.125 40000 "?" 1`) are not straightforward enough.
The only exception from this 'no-frills' plain-text approach is a future data transmitter script, that sends a JSON object via UDP, every (1...n, adjustable with decimation) n frames.

* Eye tracker confidentiality and blink state threshold adjustment (`Assets/Scripts/ExternalEyeTrackerControl.cs`, UDP port 40000)
  * The following eye tracker control variables must be read and set on demand:
    * `GazeContingentTransform2.EyeTrackingConfidenceThreshold`
    * `GazeContingentTransform2.EyesAreClosedThreshold`
* Eye tracker azimuth and elevation offset (UDP port 40001)
  * Read `GazeContingentTransform2.CurrentGazeVector` (with the query-response mechanism, and returns a **running average of gaze vector the last 10 frames** by default)
  * Set `GazeContingentTransform2.GazeVectorOffset` (note that this is a Vector2)
* Passthrough control (`Assets/Scripts/ExternalPassthroughControl.cs`, UDP port 40002)
  * This feature is useful for switching between AR/VR scenes and for orientation.
* Hand rendering control (`Assets/Scripts/ExternalHandRenderingControl.cs`, UDP port 40003)
  * This feature is for enabling/disabling the built-in hand model rendering using the headset's internal tracker.
* Adjusting the head-locked and eye-tracked objects' physical distance (`Assets/Scripts/ExternalScotomaDistanceAdjuster.cs`, UDP Port 40004)
  * This is for adjusting the depth of the eye-tracker-specific renderings, so the visual angles remain correct.
* Interpupillary distance reporter (`Assets/Scripts/ExternalInterpupillaryDistanceReporter.cs`, UDP Port 40005)
  * In the headset, there is a manual control for the interpupillary distance (IPD), which the user has to set. The problem with this is, that the participant may not be able to do this reliably, so this is an external tool to check whether the optics have moved, and they are in the right position. If the IPD is wrong, all the disparities and visual angles will be wrong, because there is plenty of distortion introduced by these planar lenses. Note that this value only can be queried, and not set, and it only returns a valid value, when the headset is worn, and not when the proximity sensor is disabled in MQDH.
* Annulus renderer (`VisionStaticAnnulus.cs`)
This script has to be loaded to child of `GazeContingentGameObject` and `HeadContingentGameObject`. It creates a visual-angle-consistent stimulus. You can enable/disable it, change its colour and size. **All units in this scripts are degrees of visual angle and NOT game units.**



The communication protocol is simple, here is an example:

* My computer is `192.168.42.79`
* The headset is `192.168.42.125`, when running a game engine.
* If I want to query the state of the eye tracker control variables, then I send an ASCII question mark, and the headset responds:
  * <192.168.42.79> -> <192.168.42.125:40000>: '?'
  * <192.168.42.127:40000> -> <192.168.42.79>: '0.9000,0.5000'
    * This implies that `EyeTrackingConfidenceThreshold` is set to 0.9, and `EyesAreClosedThreshold` is set to 0.5.
* If I want to set the eye tracker control variables, then all I have to do is:
  * Let's set `EyeTrackingConfidenceThreshold` to `0.95`
  * Let's set `EyesAreClosedThreshold` to `0.43`
    * <192.168.42.79> -> <192.168.42.125:40000>: '0.95,0.43'

...and that's it. Here is a summary of the ports and examples:

| UDP port on headset | What is it for | Example payloads |
| ------------------- | -------------- | ---------------- |
| `40000` | Eye tracker setting variable adjustment | `?`, `0.9,0.5` |
| `40001` | Eye tracker gaze offset, in Az/El degrees | `?`, `0,0`, `0.5,-0.1` |
| `40002` | Passthrough control | `0`, `1` (or literally anything else) |
| `40003` | Hand rendering control | `0`, `1` (or literally anything else) |
| `40004` | Scotoma distance adjuster (in 'metres' as per Unity units) | `0`, `0.5`, `1` |
| `40005` | Check the headset's current interpupillary distance setting | `?`, (units are in metres, so the response will be something like `0.063`) |
| `40006` | Scotoma adjustments, see next section | `?`, `1,0,0,1,5,#FF0000FF` |
| `40007` | Calibration stimulus adjustments, see next section | `?`, `1,0,0,6,10,#006400FF` |
| `40008` | **Telemetry decimation control** (`DataTransmitter.cs`; the outbound record goes to the lab sink `192.168.42.5:3431`) | `0` (stop), `5` (send one record every 5 frames) — **no reply** |
| `5000` | **OptiTrack↔Unity world alignment** (`UnityOptitrackAlignment.cs`; **no auto-run in the template** — listens until triggered) | `?` → `OK;<STATE>;<fx,fy,fz>;errMm;errDeg;attempts`, `0,0.01,0` (add fudge delta, then align), or anything else (plain trigger) |

Note on `5000`: it is deliberately **outside** the `40000`–`40007` experiment-control block — a standalone, memorable number so the same APK is findable on any lab box. It talks to the lab **streaming server** (`192.168.42.5:64923` by default, the plain-ASCII Motive front-end), not directly to Motive; the wire grammar and its invariants (LAN-only, unicast, server must be up, Matlab twin client) are documented in `UnityOptitrackAlignment.cs.md`.

To exercise any of these ports without writing C#/shelling out ad-hoc code, there is a small Python
utility in `PythonUdpBlaster/` (see `PythonUdpBlaster/README.md`).
`python3 PythonUdpBlaster 192.168.42.125 40000 "?" 1` sends `?` to the headset's port `40000`
and waits (a second, locally) for its reply, printing it to stdout; it exits non-zero on a timeout,
so it doubles as a standardised, scriptable test.

For the whole eye-tracker calibration loop as one hard-coded script (demo-grade, not for production), there is `eye_tracker_calibration_demo.py` at the repo root: `python3 eye_tracker_calibration_demo.py 192.168.42.125` walks the exact steps of the next section, printing every packet it sends and receives.

**Optional — relocate an arbitrary GameObject externally (one port per object, chosen by you).** If you want to reposition or re-rotate a GameObject from the experiment code — e.g. turn a stimulus object to a set rotation, move a spotlight, or move a wall — there is a generic pose controller, `Assets/Scripts/ExternalGameObjectControl.cs` (its full notes are in the sibling `ExternalGameObjectControl.cs.md`). This is a **generic, optional utility, not a fixed port in the table above** — it is per-instance (its `controlPort` is set *in the editor*) and an implementation may never use it. To use it:

* Create an empty GameObject (or pick the object you want to drive).
* Attach `Assets/Scripts/ExternalGameObjectControl.cs` to it.
* In the Inspector set **`controlPort`** to a port you choose and **note it down** — `5000` is already used by `UnityOptitrackAlignment`, so pick `5001`, then `5002`, `5003`…; **every object needs its own port** (two instances on one port collide, the second logs a `DUPLICATE PORT` error and goes silent).
* Attach the visual you care about (the stim mesh, the wall, the light) as a **child** of that GameObject — the script moves the parent and the children follow.
* Then drive it over UDP — `?` to query, a six-field packet to set. Default space is **world** (`transform.position`/`rotation`); set **`useLocalSpace`** to drive relative to the parent instead:

  ```
  python3 PythonUdpBlaster 192.168.42.125 5001 "?" 1                  # query  -> e.g. 0.5000,0.0000,1.0000,0.0000,30.0000,0.0000
  python3 PythonUdpBlaster 192.168.42.125 5001 "0.5,0,1,0,30,0" 0    # set pose: position (metres) + Euler (degrees); no reply
  ```

  The payload is `<x>,<y>,<z>,<rx>,<ry>,<rz>` — position in metres, orientation as Euler angles in degrees. Any frame/concept conversion is **yours** to do (this script performs none); see the sibling doc for the units, the local/world toggle, and the Euler-degree caveats.

## Scotoma and the calibration stimulus for eye tracker calibration

Both of these are rendered by `VisionStaticAnnulus.cs`, and controlled by `ExternalVisionStaticAnnulusAdjuster.cs`. They are grouped together, because they are doing the same thing, with one difference: when port `40006` is used, the annulus is adjusted that is constant **with respect to the fovea** (i.e. in this case, the  'gaze vector'), whereas when port `40007` is used, then the stimulus is constant **with respect to the head** (i.e. locked to 'CenterEyeanchor'). They have the same depth, which can be adjusted though port `40004` as needed. Note that the inner diameter of the annulus can be 0, so it can be a filled disk.

`ExternalVisionStaticAnnulusAdjuster.cs` is a bit more complex, because it handles a large number of arguments (both for the 'query-response', and 'fire and forget' way), in particular order.

| Argument position | What it is | Description | Examples |
| ----------------- | ---------- | ----------- | -------- |
| 1 | Stimulus render toggle | Enables/disables the stimulus | `0`, (and pretty much everything else is considered as 'enable') |
| 2 | Azimuth value of center | Moves the annulus horizontally (+ve is right, -ve is left) in degrees of visual angle | `-10`, `0`, `8.5` |
| 3 | Elevation value of center | Moves the annulus vertically (+ve is up, -ve is down) in degrees of visual angle | `-2`, `0`, `1.5` |
| 4 | Inner diameter | Adjusts the hole of the annulus in degrees of visual angle | `0`, `10`, `2.5` |
| 5 | Outer diameter | Adjusts the size of the annulus in degrees of visual angle | `5`, `10`, `100` |
| 6 | Colour | HTML RGBA hex colour | `#000000FF`, `#CC6412FF` |

**Note**: improperly formatted payloads are discarded. You can verify operation visually (either via casting, or wearing the headset yourself), or with the query method. The 'Azimuth' and 'Elevation' angles can either be _retinotopic_ (here, through UDP port `40006`) or _head-centered_ (here, through UDP port `40007`)

Examples, same as above - the headset is 192.168.42.125, and your computer is 192.168.42.79:

* Turn on the scotoma, have a tiny hole in it, let it appear in the fovea, and make it red
  * <192.168.42.79> -> <192.168.42.125:40006>: `1,0,0,1,5,#FF0000FF`
* Turn off the scotoma. You still can adjust its settings
  * <192.168.42.79> -> <192.168.42.125:40006>: `0,0,0,1,5,#FF0000FF`
* Create a calibration annulus where your keyboard would be. Make it large and green. But not too green.
  * <192.168.42.79> -> <192.168.42.125:40007>: `1,0,-10,6,10,#006400FF`
* Check on the state of the scotoma.
  * <192.168.42.79> -> <192.168.42.125:40006>: `?`
  * <192.168.42.125:40006> -> <192.168.42.79>: `0,0,0,1,5,#FF0000FF`

With this protocol, you can calibrate the eye tracker either with your experimental code, or just a simple script that you built up on your smartphone or microcontroller. The steps are:

* Create a calibration stimulus at a known location (azimuth, elevation, and set the depth to a typical favourite value of yours)
  * <192.168.42.79> -> <192.168.42.125:40007>: `1,0,-10,6,10,#006400FF`
  * <192.168.42.79> -> <192.168.42.125:40004>: `0.5`
* Reset the previous offset of the eye tracker
  * <192.168.42.79> -> <192.168.42.125:40001>: `0,0`
* Ask the participant to look at the stimulus, and not to blink
* Wait a little bit so enough samples are collected
* Optional: give visual feedback with the scotoma:
  * <192.168.42.79> -> <192.168.42.125:40006>: `1,0,0,1,5,#FF0000FF`
* Get the gaze vector
  * <192.168.42.79> -> <192.168.42.125:40001>: `?`
  * <192.168.42.125:40001> -> <192.168.42.79>: `1.5,-6`
* Calculate the new offset
  * We know that:
    * The stimulus is at Az/El 0°, -10°
    * The headset measures the participant at Az/El 1.5°, -6°
    * Therefore, our offset is: (0 - 1.5=) -1.5°, and  (-10 - (-6)=) 4°.
  * So the new offset is:
    * <192.168.42.79> -> <192.168.42.125:40001>: `-1.5,4`
  * ...and **verify**:
    * <192.168.42.79> -> <192.168.42.125:40001>: `?`
    * <192.168.42.125:40001> -> <192.168.42.79>: `0.1,-9.35`
* Now you can tell the participant to carry on as normal.


Repeat as necessary: the eye tracker is noisy, the participant is bored, and it's Monday morning. Don't expect things to be ideal. When done, disable, and verify

* (as needed) To turn off the calibration stimulus, but to preserve its settings:
  * <192.168.42.79> -> <192.168.42.125:40007>: `?`
  * <192.168.42.125:40007> -> <192.168.42.79>: `1,0,-10,6,10,#006400FF`
  * <192.168.42.79> -> <192.168.42.125:40007>: `0,0,-10,6,10,#006400FF`
  * <192.168.42.79> -> <192.168.42.125:40007>: `?`
  * <192.168.42.125:40007> -> <192.168.42.79>: `0,0,-10,6,10,#006400FF`

* (as needed) To turn off the scotoma, but to preserve its settings:
  * <192.168.42.79> -> <192.168.42.125:40006>: `?`
  * <192.168.42.125:40006> -> <192.168.42.79>: `1,0,0,1,5,#FF0000FF`
  * <192.168.42.79> -> <192.168.42.125:40006>: `0,0,0,1,5,#FF0000FF`
  * <192.168.42.79> -> <192.168.42.125:40006>: `?`
  * <192.168.42.125:40006> -> <192.168.42.79>: `0,0,0,1,5,#FF0000FF`

## Dependency maps

While the project is modular by design, there are _layers_ upon layers. Kind of like the OSI model. The low layers (`L0` - `L1`), by principle are hardware-dependent. So if the Quest Pro is being thrown out and replaced by other hardware (say a Pico XR headset), these probably need to be _reimplemented_. The middle layers (`L2` - `L3`) are Unity-dependent, so if, for some reason, Unity is to be replaced with something else (let's say the Build engine), then these scripts will need to be _ported_. The translation layer (`L4`) is used to interact with other hardware: get data from the motion tracker, flick a switch with an ESP32-based device, do some nice collaborative robotics, or the script for feeding game-engine-specific data to the [universal data sink](https://github.com/ha5dzs/universal-data-sink)  for example. These are unique, and probably will have to be _rewritten from scratch_ when changing hardware. The application layer (`L5`) is when _you, the user_ are, in waves of confusion and rage, reading docs, getting AI to summarise docs, and trying to make the sense of it. For external control, this is why we have `PythonUdpBlaster`, which is a local AI-accelerated reimplementation of `SimpleUdpBlaster` which had far fewer sanity checks and convenience features built in. Then, there is the 'Experiment layer' (`L7`), which is probably your Matlab `udpport` interface, and where you collect the data. And on top, is the 'Analysis layer' (`L7`), which is where all the data collected gets analysed - and would be 'L0' (i.e., 'reading csv files') in the analysis scripts.

### In a long-winded, slightly theoretic table:

| Layer | What is this | Example |
| ----------------- | -------------- | -------------- |
| `L7`: Analysis | Your script when your look at the data | R's `read_csv` |
| `L6`: Experiment | Your Matlab experiment file | `expt_workhorse.m` |
| `L5`: Application | The code you run on the headset and this documentation | `the_application.apk` |
| `L4`: Translation | Interaction with the rest of the world | `volciclab_robot_move_tcp_rpy()` |
| `L3`: Middle | Unity and its high-level internal features | `Slerp()`, quaternions, etc. |
| `L2`: Middle | Unity and its low-level internal features | `UdpClient()`, asnyc callbacks, etc. |
| `L1`: Low | Built-in hardware in the headset | Eye tracker, passthrough and their APIs, etc. |
| `L0`: Low | Core hardware stuff | Android API, rendering settings, shaders, etc. |

### In particular:

| Component (where it lives) | Requires (→) | Required by (←) |
| --- | --- | --- |
| **L5 — `PythonUdpBlaster`** (PC) | headset booted + port open | *exercises L3* (exit≠0 on timeout) |
| **L4 — OptiTrack/streamer (alignment landed 2026-11-03; streamer client on-device verified 2026-11-04; recenter *trigger* half still WIP)** | external Motive/OptiTrack HW + streaming server up | `UnityOptitrackAlignment` (alignment) · `StreamRigidBodyFromOptitrack` (continuous client) · `universe_relocator` (superseded reference) · `RecenterProbe` (diagnostic) |
| **L3 — `5000` `UnityOptitrackAlignment`** (no auto-run by default; Camera Rig) | `CenterEyeAnchor` live pose · server's one-pose reply · its own transform only (never the anchor pivots) | the L4 row — it is what licenses raw tracker-coordinate writes to land correctly in-scene |
| **L3 — `40005` `ExternalInterpupillaryDistanceReporter`** | IPD value from OVRPlugin (valid only while worn) | external lab PC |
| **L3 — `40004` `ExternalScotomaDistanceAdjuster`** | `GazeContingentTransform2` + `HeadContingentGameObject` | external lab PC |
| **L3 — `40003` `ExternalHandRenderingControl`** | `[BuildingBlock] Hand Tracking` → hand renderers | external lab PC |
| **L3 — `40002` `ExternalPassthroughControl`** | `[BuildingBlock] Passthrough` → `OVRPassthroughLayer` | external lab PC |
| **L3 — `40001` `ExternalEyeTrackerAzimuthElevationAdjuster`** | `GazeContingentTransform2` | external lab PC (calibration) |
| **L3 — `40000` `ExternalEyeTrackerControl`** | `GazeContingentTransform2` | external lab PC (UDP) |
| **L2 — outbound telemetry** (`DataTransmitter` on `[BuildingBlock] Camera Rig`, control `40008`; on-device verified 2026-11-06) | `CenterEyeAnchor` · `GazeContingentTransform2` (gaze + eyelids) · `VisionStaticAnnulus` (scotoma state) · `NtpTimeSync` (time base) · the lab `UniversalDataSink` running at `dataSinkIpAddress` | the lab sink's record file (the sink prefixes its own arrival timestamp) |
| **L2 — stimulus** (`VisionStaticAnnulus` on `Scotoma` and `EyeTrackerCalibrator`; `SilverAnnulus` = superseded reference) | `CenterEyeAnchor` distance (visual angle) · depth (via `40004`) | `DataTransmitter` (reads `Scotoma` state + position) |
| **L1 — `GazeContingentTransform2`** (on `GazeContingentGameObject`) | `OVRFaceExpressions` · eye-tracking permission | `40000` · `40001` · `40004` · stimulus |
| **L0 — `OVRFaceExpressions`** (on `GazeContingentGameObject`) | Face Tracking (OVR Manager) | `GazeContingentTransform2` (else `Update()` early-returns → no gaze) |
| **L0 — OVR Manager / Camera Rig / `CenterEyeAnchor`** | Meta XR SDK | *everything above* |

### Some (breakable) rules about how scripts interact

* Callbacks are non-blocking, and asnychronous
  * As there are lots of things happening, we don't want to cause a hang in the render loop.
  * The system kernel prioritises callbacks too, with rendering being the most important
* The same socket created within a namespace **must** be used for receiving AND transmitting
* Decimal formatting is set with `CultureInfo`, and is `en-US`.
  * This is because it is the most ASCII-friendly, which coincidentally also American.
* If a script meddles with some SDK components, these have to be added prior to calling the script
  * `FindAnyObjectByType<T>(FindObjectsInactive.Include)`
  * NOT new `<objectType>`
