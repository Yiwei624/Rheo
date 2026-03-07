加入为什么12是最好的

1.JOR Introduction

1.1 General problem: steady torque ≠ global flow (in heterogeneous stress fields)



Yield-stress fluids and weak gels exhibit a transition between solid-like and fluid-like response: below a critical stress they may sustain load without sustained flow, whereas above it continuous deformation is observed. In routine rotational rheometry, a steady measured torque is often interpreted as evidence of steady flow throughout the measurement gap. However, in geometries where the applied stress is spatially heterogeneous, steady torque does not necessarily imply global flow; instead, mechanically admissible states can exist in which yielded and unyielded regions coexist under steady rotation. This distinction is particularly important when low-stress/low-shear data are used to infer “intrinsic” yield parameters from global constitutive fits, and when low-torque regimes are dismissed as artefacts without verifying whether the gap has been fully mobilized.



Figure 1：Schematic “vane-in-cup yielding map”(https://link.springer.com/article/10.1007/s00397-014-0759-1)

Vane radius , cup radius , Height .

Stress decay .

Yield surface  separating yielded/unyielded zones.

Two regimes: partial yielded  vs fully yielded .

Optional inset: “slip vs spatial confinement” cartoon.



1.2 Stress heterogeneity in cylindrical rotation

In cylindrical rotation, torque balance imposes a radially decaying shear stress field. For steady, axisymmetric laminar flow with negligible inertia, conservation of angular momentum gives

                                                                (1),

So that

                                                             (2),

Where is the stress at the inner boundary. This inverse-square decay follows from torque transmission and is independent of constitutive assumptions(Bird, Armstrong and Hassager, 1987; Owens, Hart and McKinley, 2020).

1.3 Yield surface and the criterion for global mobilization

For a yield-stress material with yield stress , define a yield surface  by . Using Eq.(2),

                                  (3).

Full mobilization of the gap requires, giving a geometry-dependent critical inner stress

                               (4).

Whenever , the configuration is compatible with a partially yielded steady state in which an outer region remains unyielded even under steady rotation. This picture is classical in wide-gap Couette/vane interpretations and is central to large-Bingham-number rheometry, where a finite unyielded annulus is expected when the stress transmitted to large radii falls below (Lovett and Meeten, 2017).

1.4Why “narrow gap” does not automatically guarantee uniform shear

A common intuition is that a nominally narrow gap approximates uniform shear and therefore suppresses partial yielding. Equation (4) shows that this is not generally valid: global mobilization depends on the ratio , not on absolute gap width. Even when  is small,  by a finite amount, implying a non-zero stress window in which steady torque can be recorded while .

For the Bolin C-VOR C25 geometry used here, = 13.85mm and =12.50mm, so  1.23. Thus, even in a nominally small-gap C25, the inner stress must exceed  by ~23% to fully mobilize the gap; otherwise a partially yielded outer region is mechanically admissible.

1.5Slip versus spatial confinement: the key interpretive ambiguity

Vane tools are widely adopted because they can reduce sensitivity to wall slip and improve coupling compared with smooth concentric cylinders (Dzuy and Boger, 1985; Liddell and Boger, 1996; Barnes and Nguyen, 2001). Nevertheless, low-torque regimes in vane-in-cup data—especially for structured soft solids—are still frequently interpreted as slip-dominated artefacts. The difficulty is that a near-wall “inactive” region is not uniquely diagnostic of slip. Slip implies failure of the no-slip boundary condition and a velocity discontinuity at the solid boundary, whereas spatial confinement arises from radial stress decay and remains compatible with no-slip boundaries. In partially yielded states, the effective outer boundary becomes the internal yield surface at , so the torque is controlled by the size of the yielded annulus rather than by the cup wall condition (Lovett and Meeten, 2017).

This distinction directly impacts parameter extraction. If partially yielded states are included in “steady flow curves,” global constitutive fits (e.g. Bingham or Herschel–Bulkley) can absorb geometry-dependent mobilization effects into apparent yield stresses and viscosities, yielding values that are not intrinsic material parameters but rather reflect whether the gap was fully mobilized (Lovett and Meeten, 2017).

1.6 Why weak gels, and why yogurt?

Weak gels are a stringent test case because structural heterogeneity and time-dependent breakdown/recovery occur on experimentally relevant timescales. Yogurt is a representative thixotropic weak gel formed by acid-induced aggregation into a space-spanning protein network. It displays yield-like behavior, strong shear thinning, and pronounced hysteresis between ramp-up and ramp-down flow curves. Yogurt is also predominantly subjected to low-stress/low-shear deformations during processing (start-up pumping, filling) and consumption (spooning and oral processing), meaning that the low-shear regime is not merely a measurement nuisance but the regime of primary relevance.

Food-engineering studies have long treated yogurt as a challenging thixotropic material for flow prediction, including pressure-drop calculations in processing flows (Schmitt et al., 1998). More recent studies comparing thixotropic yield-stress materials explicitly report that yogurt can remain strongly transient even after long shearing times, motivating the use of controlled residence times in hysteresis-loop protocols (see discussion of yogurt transience in Phys. Fluids 36, 023107 (2024)).

1.7 3D-printed vane geometries as a controlled perturbation

Recent stereolithographic 3D printing enables low-cost fabrication of bespoke vane geometries with controlled blade number and perimeter complexity. Owens, Hart and McKinley (2020) introduced bespoke fractal 3D-printed vanes and textured cups, established design criteria, and demonstrated that multi-armed 3D-printed vanes can reproduce Newtonian calibration oils with low error and provide robust yield-stress measurements in challenging materials. This advances the practical accessibility of vane rheometry by enabling systematic geometric variation at low cost.

However, an unresolved point remains: if low-torque regimes persist even when coupling is improved and slip is mitigated, then the regime may reflect spatial confinement rather than slip. Conversely, if slip dominates, increased roughness and blade number should remove the plateau without requiring a yield-surface interpretation. Controlled variation of blade number in 3D-printed vanes therefore provides a practical route to interrogate the origin of low-torque regimes through a systematic geometric perturbation.

1.8 Dimensionless regime classification (bridge to Theory section)

To connect experimental datasets directly to the global-mobilization condition, it is useful to define a dimensionless parameter comparing the applied inner stress to the critical mobilization stress:

                            (5).

The parameter  separates two mechanically distinct regimes: (partially yielded ; spatially confined shear) and (fully yielded; full-gap mobilization). This provides a state-aware framework for interpreting low-shear vane data and assessing whether apparent yield parameters extracted from global fits are representative of intrinsic material response or are contaminated by incomplete mobilization.

Accordingly, the theoretical framework that follows formalizes the relation between torque, yielded-annulus extent, and the regime classification in terms of .

Objectives and scope

Motivated by these considerations, the present study re-examines steady-shear vane-in-cup measurements of a commercial yogurt using 3D-printed vanes with 4, 12, and 24 blades, alongside a printed replica and a commercial metal C25 vane. The objectives are:

Benchmarking and validation: validate torque-to-stress conversion and low-shear measurement fidelity using a Newtonian silicone oil benchmark, consistent with the calibration philosophy for 3D-printed vanes (Owens, Hart and McKinley, 2020).

State-aware interpretation of yogurt data: quantify geometry dependence and hysteresis in up/down sweeps, and assess how conventional fits (e.g. Bingham/power-law) yield geometry-dependent apparent parameters when partially yielded states are included (Lovett and Meeten, 2017).

Regime identification using a dimensionless criterion: map experimental data onto  (and/or ) to distinguish partially and fully yielded regimes and to identify the transition from spatial confinement to full-gap mobilization as a function of imposed conditions.

By embedding standard vane measurements within an explicit global-mobilization framework, this work clarifies the physical origin of low-torque regimes in a representative weak gel and provides a principled basis for comparing blade-number effects beyond slip-only interpretations.

2. Theoretical framework

2.A. Stress distribution and torque–stress relation (Owens, Hart and McKinley, 2020).

Consider a vane-in-cup geometry of height , with inner radius (effective vane radius) and outer cup radius . Under steady, axisymmetric, inertialess conditions, torque balance implies

                              (6),

Where is the stress at the vane surface.

The torque transmitted through a cylindrical surface of radius  is

                               (7).

Using Eq.(6),  is dependent of , which is equivalent to conservation of angular momentum. Evaluating Eq. (7) at  gives an expression to convert measured torque to the inner-wall stress:

                                  (8).

2.B. Yield surface and global mobilization criterion

For a yield-stress material with yield stress , define a yield surface  by . From E1.(6),

                                  (9).

Two mechanically distinct regimes follow immediately:

Partially yielded (spatially confined) regime:

Fully yielded (globally mobilized) regime:

The stress at the vane required for full-gap mobilization is therefore​

                              (10).

This motivates two equivalent dimensionless indicators for regime classification:

                           (11).

Thus:

(or ):partially yielded steady configuration is mechanically admissible

(or ):full-gap mobilization

[Fig. 2 here — “Regime map”] 部分屈服区

2.C. Why apparent flow curves become geometry dependent in the partially yielded regime

2.C.1. Dissipation is confined to the yielded annulus

In the partially yielded regime, the region  is is unyielded and does not sustain continuous shear. The effective “outer boundary” for the flowing region is therefore  rather than . This is the key point: the cup wall is dynamically irrelevant to dissipation as long as .

Consequently, any attempt to interpret the measurement using a global “gap-averaged” shear rate (as in standard Couette data reduction) will mix two physically different states:

a locally sheared inner annulus

a solid-like outer region

This immediately explains why low-shear steady data can show strong geometry dependence even when slip is suppressed: the measured torque reflects how much of the gap is mobilized, not merely the intrinsic constitutive response.

2.C.2. Torque sensitivity near the mobilization threshold

Near the mobilization threshold (),small changes in  produce comparatively large changes in  because

                              (12).

Thus, the effective flowing thickness  can vary strongly with stress in the low-stress window. This provides a mechanistic explanation for:

Extended low-torque/low-stress “plateaus”,

Strong sensitivity to geometry and surface condition,

Pronounced path dependence in up/down sweeps in thixotropic gels.

2.D. Regime-dependent meaning of “yield stress” extracted from global fits

In practice, yield parameters are often extracted from global constitutive fits such as Bingham or Herschel–Bulkley using a single “apparent” shear rate and stress. In the partially yielded regime, these fitted parameters become state- and geometry-dependent because the dataset does not correspond to globally mobilized flow.

To emphasize this point, we distinguish:

Intrinsic yield stress  :the local criterion for yielding (entering Eq. (9)–(10))

Apparent yield stress :the intercept extracted from a global fit to

When ,  can absorb the effect of incomplete mobilization (i.e., the dependence of  on ) and therefore varies across geometries and data windows. Only when  is it defensible to interpret steady flow-curve parameters as representative of an intrinsic material response in the VIC geometry.

[Fig. 3 here — “Fitted yield stress vs regime”] 直接展示“拟合屈服应力的几何依赖”来自 regime 混合。

2.E. Practical data-reduction workflow used in this study

For each datapoint in a steady sweep:

Convert measured torque  to inner stress using Eq.(8).

Obtain  (intrinsic yield stress) from a consistent procedure (e.g., a chosen fit window, or a reference geometry).

Compute  using Eq.(10).

Classify the point using  (Eq.(11)) and/or compute .

Report flow curves with regime annotation: partially yielded () vs fully yielded().

This regime-aware mapping enables direct comparison of vane geometries without conflating boundary artefacts and spatial confinement.

3.Materials and Methods

3.1 Materials

3.1.1 Newtonian calibration fluid



A Newtonian silicone oil with nominal kinematic viscosity of 100 cSt was used as a benchmark fluid to validate torque transmission and the data-reduction procedure across all geometries. The oil was equilibrated at the test temperature prior to measurement.

[Fill: supplier, product code, density if needed, temperature]

3.1.2 Weak gel sample (yogurt)

A commercial stirred yogurt was used as a representative thixotropic weak gel. Yogurt was stored at [5 °C] and brought to the test temperature for at least [X min] prior to loading. Each measurement used a fresh aliquot from the same production batch [or specify batch ID/date].

[Fill: brand/type, fat/protein %, batch ID if available]

3.2 Rheometer and temperature control

Measurements were performed on a rotational rheometer [model, manufacturer] equipped with a vane-in-cup (VIC) fixture and a temperature control unit. The temperature was maintained at [T = xx °C] and verified by [instrument sensor / external thermometer]. A solvent trap or environmental cover was used [yes/no] to minimise evaporation.

[Fill: instrument model (e.g., Bohlin CVOR), temperature cell type, temperature stability]

3.3 Vane-in-cup geometries and fabrication

3.3.1 Tested geometries

Five VIC inner tools were tested:

A 4-blade 3D-printed vane (outer diameter 𝐷𝑣= [mm], height 𝐻= [mm]).

A 12-blade 3D-printed vane (same outer diameter and height).

A 24-blade 3D-printed vane (same outer diameter and height).

A commercial metal C25 vane supplied by the rheometer manufacturer.

A 3D-printed PLA replica of the C25 vane with nominally matched dimensions.

All measurements used the same cup with inner radius 𝑟2= [mm] and working immersion depth 𝐻= [mm].

[Fig. M1 here: photo montage of tools + key dimensions table] (optional but recommended for JOR)



3.3.2 3D printing and surface characteristics

Printed vanes were fabricated using stereolithography [or FDM; specify method] in PLA [or resin type]. After printing, supports were removed and surfaces were cleaned using [method]. Surface roughness was not actively polished; thus printed tools exhibited higher microscale roughness than the commercial metal tool.

Important: the printed C25 replica was intentionally “dimensionally nominal” but may exhibit small deviations in effective radius due to printing tolerances. Key dimensions (𝑟1, blade thickness) were measured using [calipers/microscope] with resolution [x].

[Fill: printer model, layer height, post-cure, measurement resolution]



4. Results

4.1 Validation of conversion factors and low-torque fidelity using a Newtonian benchmark

To establish the reliability of torque-to-stress and rotation-to-shear-rate conversion prior to testing a weak gel, steady-shear measurements were first conducted using a Newtonian silicone oil (100 cSt) across all tested geometries. The resulting viscosity–shear-rate curves collapse over the experimentally robust range, indicating that the adopted conversion factors are internally consistent and that the different tools transmit torque in a physically credible manner under Newtonian conditions.



Figure 2：100 cSt silicone oil viscosity vs shear rate

Table 1：Newtonian benchmark error metrics

Quantitatively, the 12-blade vane provides the closest agreement with the reference measurement, while larger deviations are observed for other geometries, particularly in the lowest shear-rate region where torque resolution and baseline drift become increasingly influential. Importantly, the agreement observed in the moderate shear-rate regime demonstrates that subsequent geometry dependence observed in yogurt cannot be attributed to a systematic failure of the conversion procedure. Rather, any pronounced low-shear divergence in the weak-gel dataset must be explained by material physics and/or regime-dependent flow states.



4.2 Geometry dependence of yogurt flow curves is concentrated at low shear



Steady-shear measurements of yogurt reveal strong geometry dependence at low shear rates, while converging behaviour is recovered at higher shear rates. Across all fixtures, the stress–shear-rate response exhibits three qualitative regimes: (i) a low-shear plateau-like response, (ii) a transition region, and (iii) a high-shear shear-thinning regime. However, the extent and magnitude of the low-shear regime varies markedly between geometries.



Figure 3：Yogurt shear stress vs shear rate up/down sweeps



Figure 4：Yogurt viscosity vs shear rate up/down sweeps



The low-shear plateau is most pronounced for the quasi-cylindrical configurations (e.g., C25 and high blade-count vanes), whereas the 12-blade vane transitions earlier toward increasing stress with shear rate. The 4-blade vane exhibits larger scatter and a more pronounced separation between up- and down-sweeps. The geometry dependence is most apparent at low shear rates; as shear rate increases, the curves progressively converge, suggesting that the dominant dissipation mechanism changes with increasing stress and that a geometry-controlled regime boundary exists.



The up–down separation indicates significant path dependence consistent with structural breakdown and recovery. Notably, the magnitude of hysteresis is also geometry dependent, implying that the effective sheared volume and/or the extent of mobilization differs across tools in the low-shear regime.

4.3 Apparent yield parameters from global fits are geometry dependent

To quantify the extent to which conventional constitutive descriptions capture the data, the yogurt flow curves were fitted using common engineering models (Bingham and power-law) over prescribed shear-rate windows. The fitted parameters, particularly the yield-stress-like intercept in the Bingham form, show strong geometry dependence.

Table 2 and 3：Bingham fit parameters and Power-law fit parameters



Figure 5： vs geometry

The apparent yield stress extracted from global fits varies by a factor that far exceeds experimental repeatability, indicating that the fitted “yield stress” is not an intrinsic material constant under the tested conditions. Instead, these values encode a mixture of true material response and geometry-dependent flow state. This observation motivates the regime-aware analysis that follows: the same dataset may contain both partially yielded and fully yielded configurations, and global fitting across these states naturally produces geometry-dependent apparent parameters.

4.4 Regime mapping demonstrates persistent partially yielded steady states in nominally narrow-gap geometries

Using the spatial-yielding framework introduced in Section 2, each datapoint can be mapped onto the dimensionless global-yielding parameter , or or equivalently to the normalized yield radius . This mapping enables explicit separation of partially yielded ( or ) and fully yielded (or )states within the same steady-sweep dataset.



Figure 6a:  vs shear rate             Figure 6b: shadow area for partial yielded

The regime mapping reveals that a substantial fraction of the low-shear dataset resides in ,spanning multiple decades in shear rate. Crucially, this partially yielded window persists even for nominally small-gap configurations such as C25, demonstrating that narrow-gap VIC fixtures do not automatically guarantee full-gap mobilization. The existence of a broad, mechanically admissible partially yielded steady regime provides a direct physical interpretation of the low-shear torque plateau: the measured torque reflects dissipation within a yielded inner annulus while an outer region remains below the local yield criterion.



This result also explains why geometry dependence is strongest at low shear rates. In the partially yielded regime, differences in stress transmission efficiency and local mobilization extent translate directly into differences in the effective sheared volume, whereas once  is achieved, the entire gap participates in flow and the measured response becomes less sensitive to the specific tool geometry.



4.5 Regime-dependent torque ratio inversion indicates a mechanism transition near full mobilization



A stringent test of the regime interpretation is provided by comparing geometries that are nominally identical in size but differ in material and surface characteristics (e.g., metal C25 versus 3D-printed PLA C25). The torque ratio  is plotted as a function of  (or equivalently ).



Figure 7a: common                         Figure 7b: cup-specific

The torque ratio exhibits a clear regime dependence and undergoes a systematic change in trend as  approaches unity. In the partially yielded regime(), torque differences are large, consistent with dissipation being controlled primarily by the extent of the yielded annulus. Here, small differences in effective coupling or mobilization can produce substantial torque changes because the outer region does not participate in flow.



As the yield radius approaches the cup wall (), the torque ratio transitions toward a different behaviour. In the fully yielded regime (),the entire gap is mobilized and the influence of boundary coupling and surface condition becomes comparatively more direct. The observed change (and, where present, inversion) of  across () therefore constitutes an experimental marker of a transition from spatially confined shear to boundary-controlled dissipation, rather than a simple monotonic “more slip vs less slip” interpretation.

The persistence of this trend under alternative definitions of  (common versus geometry-specific) demonstrates that the conclusion is robust to the particular yield-stress estimation protocol.



4.6 Hysteresis is amplified in the partially yielded regime



To quantify path dependence, the difference between the up- and down-sweep curves was analysed using a hysteresis metric (e.g., loop area, thixotropic index, or a normalized stress difference at matched shear rates). The resulting measure shows that hysteresis is most pronounced in the same low-shear region identified as partially yielded by the regime mapping.



Figure 8：Hysteresis metric vs shear rate( this graph as proxy)

In the partially yielded regime, hysteresis reflects the combined effects of structural evolution and mobilization extent. Because the yielded annulus thickness is highly sensitive to stress near the mobilization threshold, modest changes in structure (and hence in effective  or local fluidity) can produce large differences in the mobilized region between up and down sweeps. Once the fully yielded regime is reached, the effective sheared volume saturates at the full gap and the geometry dependence of hysteresis is reduced.



This regime-dependent amplification of hysteresis is therefore consistent with the spatial confinement interpretation and provides an additional, independent signature supporting the existence of partially yielded steady states in the low-shear window.



4.7 Direct visual evidence: adhered outer layer is consistent with spatial confinement



Following steady-shear tests, the cup wall and tool surfaces were visually inspected. A persistent annular residue of yogurt adhered to the cup wall was observed, with substantial differences in residue extent between geometries. In addition, the mass of residual yogurt retained on the tool/cup after testing was quantified.



Figure 9a: Comparison of yogurt stick on cup inner surface(12/24/4/C25/PLA C25)

Fig. 9b：残留质量（或残留比例）vs geometry 的柱状图

The presence of a continuous adhered layer indicates strong wall adhesion under these conditions, and therefore does not support a simple picture in which low-torque plateaus arise solely from interfacial slip. More importantly, the residue pattern is qualitatively consistent with the spatial confinement framework: in the partially yielded regime, an outer region can remain below the local yield stress and thus experiences negligible sustained shear, making it plausible for an unsheared layer to persist after the test. Geometries that promote more quasi-cylindrical coupling (e.g., high blade-count or C25-like configurations) exhibit more pronounced near-wall residue, consistent with a broader partially yielded window inferred from the regime mapping.



While visual inspection alone cannot uniquely diagnose slip, the agreement between residue observations, regime mapping (), and the regime-dependent torque-ratio transition provides a coherent evidence chain supporting the interpretation that low-shear plateaus in yogurt VIC measurements correspond to mechanically admissible partially yielded steady states.



5.Discussion

5.1 What the Newtonian benchmark does—and does not—tell us



The Newtonian silicone-oil benchmark serves a specific purpose: it isolates the integrity of torque transmission and the correctness of data reduction from weak-gel physics. The collapse of viscosity data across multiple geometries in the robust shear-rate range confirms that the torque-to-stress and rotation-to-shear-rate conversions are internally consistent and that the 3D-printed vanes can reproduce a reference Newtonian response, consistent with prior calibration-focused work on bespoke printed geometries (Owens, Hart and McKinley, 2020). Importantly, this benchmark also frames the role of low-shear deviations: while torque resolution can contribute to scatter at the smallest torques, the systematic, geometry-dependent trends observed in yogurt extend far beyond the narrow region where instrument limits dominate. Therefore, the yogurt results must be interpreted in terms of flow-state physics rather than conversion artefacts.



A further implication is methodological. Because the 12-blade geometry performs best under Newtonian conditions, it provides a defensible reference for subsequent regime mapping (e.g., for defining a common  or selecting a robust “fully mobilized” window). This does not establish 12 blades as universally optimal; rather, it establishes that the 12-blade tool provides the most reliable access to the low-torque measurement space in the present experimental setup.



5.2 Geometry dependence at low shear reflects a change in the dissipation mechanism, not merely constitutive variation



The yogurt flow curves show a striking feature: geometry dependence is concentrated at low shear rates and gradually diminishes at higher shear rates where curves converge. If the primary difference between geometries were a simple change in the measured constitutive response (e.g., a systematic offset in stress due to mis-calibration), the discrepancy would be expected to persist across the shear-rate range. Instead, the observed pattern is consistent with a regime transition in which the dominant dissipation mechanism changes as stress increases.



In the framework of spatial yielding, low-shear steady states can correspond to partially yielded configurations in which dissipation is confined to a yielded inner annulus while an outer region remains unyielded. As stress increases and the yield surface approaches the cup wall, the effective flowing domain expands until global mobilization is achieved. Only after this point does the measured response more closely represent a full-gap flow curve. This provides a natural interpretation of the empirical observation that geometry differences fade at high shear: once the entire gap is mobilized, the measured torque reflects bulk dissipation across a fixed domain, reducing sensitivity to how that domain was accessed.



This reasoning also clarifies a frequent interpretive pitfall in weak-gel rheometry: low-shear plateaus are often treated as slip-dominated artefacts. However, a near-wall low-shear region is not uniquely diagnostic of slip; it can also arise from heterogeneous stress transmission in the absence of interfacial failure (Barnes and Nguyen, 2001; Lovett and Meeten, 2017). In the present dataset, the concentration of geometry dependence at low shear, combined with the regime mapping (Section 5.4), supports the view that spatial confinement is a primary contributor.



5.3 Why global fits produce geometry-dependent “yield stresses”



Global constitutive fits (Bingham, Herschel–Bulkley, or power-law variants) implicitly treat the dataset as a single mechanical state described by a unique relationship .The strong geometry dependence of fitted parameters—especially the yield-like intercept—indicates that this assumption is violated for yogurt in the tested low-shear window.



Within the spatial-yielding framework, this behaviour is expected. When , the effective flowing domain is not the full annulus  but a truncated annulus . Any global fit performed on  versus an apparent shear rate will therefore absorb mobilization effects (i.e., how  changes with stress and history) into fitted parameters. In that sense,  becomes a hybrid quantity reflecting both material properties and the extent of mobilization. Only when  is it defensible to interpret fitted parameters as closer to intrinsic material response in the VIC geometry.



This point is not merely methodological: it impacts how “yield stress” values reported for weak gels should be compared across studies. If different fixtures access different fractions of the partially yielded regime, they will naturally report different apparent yield stresses even for the same material. This can create a false impression of sample-to-sample variability that is, in fact, a state- and geometry-selection effect. Similar concerns have been raised in the wider yield-stress rheometry literature, where the interpretation of low-stress steady data requires explicit attention to heterogeneous stress fields and yielding conditions (Lovett and Meeten, 2017; Barnes and Nguyen, 2001).



5.4 Partial yielding persists in nominally narrow-gap vane geometries: the key physical result



A central contribution of this work is the explicit demonstration that partially yielded steady states occupy a substantial fraction of the low-shear dataset even in nominally narrow-gap VIC configurations. While partial yielding is well established in wide-gap Couette settings, practical rheometry often relies on an implicit “narrow gap ≈ uniform shear” assumption. The regime mapping shows that this assumption fails in a mechanically predictable way: global mobilization depends on , and a finite stress window exists in which steady torque is compatible with . This is not a transient artefact but a mechanically admissible steady configuration.



The key implication is interpretive. In weak gels such as yogurt, the low-shear plateau should not be automatically discarded as noise; nor should it be automatically attributed to slip. Instead, it should be understood as a regime in which the measured torque is dominated by dissipation within a partially mobilized inner annulus, with the size of that annulus being sensitive to geometry, surface condition, and material history. This offers a consistent physical explanation for why different vane designs can report different low-shear behaviour under otherwise identical protocols.



5.5 Torque-ratio inversion as a regime-transition marker: spatial confinement to boundary-controlled dissipation



The regime-dependent torque ratio between printed and metal C25 fixtures provides a stringent test of the mechanism. In the partially yielded regime, torque differences are large and the ratio reflects differences in mobilization efficiency and the extent of the yielded annulus. As the system approaches full mobilization (, the torque ratio changes trend and can invert, indicating that the controlling mechanism has changed.



This behaviour is difficult to rationalize using a purely slip-based interpretation. If slip were the sole contributor, one would expect torque ratios to vary monotonically with surface roughness and coupling strength () rougher surfaces reducing slip and increasing torque) across the shear-rate range. Instead, the observed regime-dependent change implies that surface effects and geometric coupling play qualitatively different roles before and after global mobilization. In the partially yielded regime, the cup wall is dynamically “inactive” because it is separated from the flowing region by an unyielded annulus; in the fully yielded regime, the cup wall becomes dynamically relevant, and boundary conditions can influence dissipation more directly. This provides a physically coherent explanation for why the printed tool can yield lower torque in the partially yielded regime yet higher torque once fully mobilized.



Importantly, the robustness of this trend under alternative yield-stress estimation protocols (common versus geometry-specific ) indicates that the torque-ratio transition is not an artefact of how is  chosen, but a feature intrinsic to the regime structure of the measurement.



5.6 Hysteresis and thixotropy: why path dependence is amplified in



The amplification of hysteresis in the partially yielded regime is consistent with the combined roles of thixotropy and spatial mobilization. For a thixotropic weak gel, structural breakdown reduces resistance to flow, while recovery can occur on comparable timescales. When , the size of the mobilized region is sensitive to stress and to the effective yield criterion. Consequently, modest differences in structure between up- and down-sweeps can translate into substantial differences in the mobilized annulus thickness , magnifying the observed hysteresis.



Once , the mobilized region saturates at the full gap, and the sensitivity of torque to mobilization extent is reduced. While thixotropy can still produce hysteresis, the regime mapping predicts a diminished geometry dependence, consistent with the convergence of flow curves at higher shear. This reinforces the interpretation that low-shear hysteresis is not solely a constitutive property but also reflects state-dependent mobilization under heterogeneous stress.



5.7 Visual residue: consistent with spatial confinement and strong adhesion, not a standalone slip diagnostic



The observation of an annular adhered layer on the cup wall provides qualitative evidence that is consistent with the spatial confinement picture. In the partially yielded regime, the outer region is predicted to remain below the local yield criterion and thus experiences negligible sustained shear. In a strongly adhesive material such as yogurt, this unyielded outer region can persist as a visible residue after testing. The fact that residue extent varies systematically across geometries further supports a coupling between geometry-dependent mobilization and near-wall inactivity.



At the same time, it is important to emphasize that visual adhesion alone is not a definitive slip test: adhesion can coexist with local slip under some conditions, and residue formation depends on multiple factors including surface energy, roughness, and structural rebuilding. The strength of the present evidence lies in the coherence of multiple independent signatures: (i) regime mapping, (ii) torque-ratio transition near , (iii) geometry-dependent low-shear behaviour, and (iv) residue observations. Together, these form a consistent evidence chain favouring spatial confinement as a primary mechanism in the low-shear regime.



5.8 Implications for vane design and “why 12 blades works” in this framework



A practical outcome of the regime interpretation is a mechanistic explanation of why the 12-blade vane provides the most reliable yogurt measurements in the present study. The key point is not that 12 blades “eliminate” partial yielding in an absolute sense, but that the 12-blade geometry accesses the fully mobilized regime at lower imposed conditions than the more quasi-cylindrical (high blade-count or C25-like) configurations, while also providing more stable coupling and lower scatter than the 4-blade vane.



Within the regime-aware framework, an “optimal” vane for weak-gel steady sweeps is one that (i) provides robust low-torque transmission (as verified by the Newtonian benchmark), (ii) minimizes scatter and hysteresis artefacts induced by poor coupling, and (iii) reaches  over the experimentally accessible stress window so that intrinsic parameter extraction is defensible. The present results indicate that the 12-blade design provides the best balance among these requirements for yogurt under the tested conditions, whereas the 4-blade vane suffers from reduced effective coupling and the 24-blade/C25-like tools remain in the partially yielded regime over a broader low-shear window.



This interpretation reframes “best geometry” as a regime-accessibility problem: blade number does not merely tune coupling, but governs whether fully mobilized flow is experimentally reachable within practical torque and shear-rate ranges.



5.9 Practical relevance: low-shear physics as the regime of use, not a nuisance



Finally, the present findings clarify the physical meaning of low-shear data in weak gels in a way that is directly relevant to industrial handling. Many practical deformations experienced by yogurt—such as start-up in pumping, filling, and consumer spooning/oral processing—operate in low-stress/low-shear conditions where partial mobilization is plausible. The regime-aware interpretation therefore suggests that low-shear measurements should not be treated as intrinsically unreliable. Instead, they should be reported with explicit regime classification ( or ), distinguishing whether the measurement represents a fully mobilized flow curve or a partially yielded steady configuration. This provides a more physically consistent basis for comparing formulations, predicting handling behaviour, and designing measurement protocols that target the regime of interest.



6.Conclusions



This study re-examined steady-shear vane-in-cup (VIC) rheometry of a representative weak gel (yogurt) using 3D-printed vanes with 4, 12, and 24 blades, together with printed and metal C25 fixtures, and interpreted the resulting torque data within an explicit spatial-yielding framework. The main conclusions are:



Calibration and data-reduction fidelity were established using a Newtonian benchmark.

Measurements on a 100 cSt silicone oil demonstrated consistent torque–stress and rotation–shear-rate conversion across geometries over the robust measurement range, supporting the use of 3D-printed vanes as low-cost, systematically tunable fixtures for controlled rheometric comparison.



Yogurt flow curves exhibit strong geometry dependence concentrated at low shear, and global constitutive fits yield geometry-dependent “yield” parameters.

Conventional Bingham/power-law fits applied to the full dataset produced markedly different apparent yield parameters across geometries, demonstrating that low-shear VIC datasets cannot be assumed to correspond to a single globally mobilized flow state.



Partially yielded steady states persist even in nominally narrow-gap VIC geometries.

Mapping the data onto a dimensionless global-mobilization criterion(, equivalently ) revealed a substantial experimentally accessible window with , indicating that steady torque is compatible with incomplete gap mobilization in practical “small-gap” fixtures such as C25.



A regime transition near  is identified experimentally.

The torque ratio between printed and metal C25 fixtures changes systematically across , providing an experimental marker of a transition from spatially confined shear (partial yielding) to fully mobilized, boundary-influenced dissipation.



Blade number controls access to fully mobilized flow within practical stress windows, explaining the performance of the 12-blade vane.

The 12-blade vane provides the most reliable access to the fully yielded regime under the tested conditions while avoiding the increased scatter associated with the 4-blade tool and the extended partial-yield window observed in more quasi-cylindrical (high blade-count/C25-like) configurations. This reframes “optimal geometry” as a regime-accessibility problem rather than a slip-only issue.



Overall, these results clarify the physical meaning of low-shear VIC measurements in weak gels: low-torque regimes should not be treated solely as slip artefacts, but can correspond to mechanically admissible partially yielded steady configurations. The dimensionless mobilization criterion introduced here provides a practical basis for (i) separating data suitable for intrinsic constitutive fitting from data dominated by incomplete mobilization and (ii) comparing vane geometries and surface conditions in the regime most relevant to processing and consumer handling of weak gels.



Reference:

Owens, C.E., Hart, A.J. and McKinley, G.H. (2020) ‘Improved rheometry of yield stress fluids using bespoke fractal 3D printed vanes’, Journal of Rheology, 64(3), pp. 643–??? (article starts at 643). doi:10.1122/1.5132340.

Lovett, S. and Meeten, G.H. (2017) Wide-gap Couette and vane rheometry for viscoplastic fluids. Schlumberger Gould Research Report (Mon 18 April 2017).

（内部报告 Harvard 也允许这样写；如果你后续要把它换成正式期刊版本也可以。）

Bird, R.B., Armstrong, R.C. and Hassager, O. (1987) Dynamics of Polymeric Liquids. New York: Wiley.

（你也可以只在 theory 推导处用，不一定在 intro 用。）

Barnes, H.A. and Nguyen, Q.D. (2001) ‘Rotating vane rheometry – a review’, Journal of Non-Newtonian Fluid Mechanics, 98, pp. 1–14.

Dzuy, N.Q. and Boger, D.V. (1985) ‘Direct yield stress measurement with the vane method’, Journal of Rheology, 29, pp. 335–347.

Liddell, P.V. and Boger, D.V. (1996) ‘Yield stress measurements with the vane’, Journal of Non-Newtonian Fluid Mechanics, 63, pp. 235–261.

Schmitt, L., Ghnassia, G., Bimbenet, J.J. and Cuvelier, G. (1998) ‘Flow properties of stirred yogurt: Calculation of the pressure drop for a thixotropic fluid’, Journal of Food Engineering, 37(4), pp. 367–388.

[Phys. Fluids 36, 023107 (2024) — 你这篇需要补全作者信息]
