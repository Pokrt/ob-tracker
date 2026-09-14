from check import free_spots
assert free_spots('<strong>Volná místa: </strong> 0 <br />') == 0
assert free_spots('<strong>Volná místa: </strong> 3 <br />') == 3
print("ok")
