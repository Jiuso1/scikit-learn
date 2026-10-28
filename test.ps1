$n = $args[0]

$coordinatorScriptBlock = {
  C:\sklearn-env\Scripts\Activate.ps1
  py C:\Users\jesus\Documents\python\Linkference\scikit-learn\coordinator.py
}

$workerScriptBlock = {
  C:\sklearn-env\Scripts\Activate.ps1
  py C:\Users\jesus\Documents\python\Linkference\scikit-learn\worker.py
}

Start-Job $coordinatorScriptBlock

for ($i = 0; $i -lt $n; $i++) {
  Start-Job $workerScriptBlock
}

While (Get-Job -State "Running")
{
  Start-Sleep 10
}

Get-Job | Receive-Job
