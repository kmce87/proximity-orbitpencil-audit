import LeanPortDeployedDomainBridge4096
import LeanPortSameKeyFamily

/-!
Lane A falsification gate: inspect transitive axioms of concrete field cardinality,
deployed-degree transfer, and the fixed-line cardinality theorem.
This is an audit candidate; compilation and stdout must be checked before
claiming any axiom status. It does not establish external MCA equivalence.
-/

#print OrbitPencilLiftSameKey.concrete_sextic_card
#print axioms OrbitPencilLiftSameKey.concrete_sextic_card
#print OrbitPencilLiftDeployedDomain4096.DeployedBad
#print OrbitPencilLiftDeployedDomain4096.supportWise_to_deployed
#print axioms OrbitPencilLiftDeployedDomain4096.supportWise_to_deployed
#print OrbitPencilLiftDeployedDomain4096.exists_many_deployed_bad_slopes
#print axioms OrbitPencilLiftDeployedDomain4096.exists_many_deployed_bad_slopes
