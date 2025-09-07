
# French : 
## Pour les administrateurs de l'Active Directory
## Lister les comptes dont le mot de passe n'expire jamais et mettre à jour pour que le mot de passe expire

# English : 
## For Active Directory Administrators
## List accounts whose passwords never expire and update them so that the password does expire

$Date_Day = Get-Date -UFormat %Y%m%d
$Path = "z:\export"
$Results_File = $Path + "\" + $Date_Day + " Maj_Cptes_PwdNeverExpires.csv"

# French : Lister les comptes dont le mot de passe n'expire jamais, et afficher le nombre
# English : List accounts whose passwords never expire, and display the number
$List_Accounts = $Null
$List_Accounts = "OU=LAB,DC=sun,DC=local" | ForEach { Get-ADUser -Filter * -Properties * -SearchBase $_ | Sort Surname} | Select CanonicalName, Description, DistinguishedName, Enabled, GivenName, LastLogon, LastLogonTimestamp, Mail, Name, PasswordExpired, PasswordLastSet, PasswordNeverExpires, PasswordNotRequired, SamAccountName, Surname, whenCreated, whenChanged
$List_Accounts.count


Cls

# Delete the Results_File if exists
If (Test-Path $Results_File) { 
    Remove-item -path $Results_File -force
}

# Create the Results_File with header line
Add-Content -Path $Results_File -Value ("Login" + ";" + "Name_Firstname" + ";" + "OU" + ";" + "Pwd_LastSet" + ";" + "LastLogon" + ";" + "LastLogonTimeStamp" + ";" + "Enabled")

# Loop through accounts to find those whose field PasswordNeverExpires is $False, and update it to $True
# And export the account in the Results_File
$Nb = 0
Foreach ($member in $List_Accounts) {

    $Cpte_AD_Session = $member.SamAccountName
    $Cpte_AD_CanonicalName = $member.CanonicalName
    $Cpte_AD_DistinguishedName = $member.DistinguishedName
    $Cpte_AD_Enabled = $member.Enabled
    $Cpte_AD_Mail = $member.Mail
    $Cpte_AD_Name = $member.Name
    $Cpte_AD_lastLogon = $member.LastLogon
    $Cpte_AD_lastLogon_Conv_Fr = [datetime]::FromFileTime($Cpte_AD_lastLogon).ToString('dd/MM/yyyy')
    $Cpte_AD_lastLogon_Conv = [datetime]::FromFileTime($Cpte_AD_lastLogon)
    If ($Cpte_AD_lastLogon_Conv_Fr -eq "01/01/1601") {$Cpte_AD_lastLogon_Conv_Fr = "Jamais"}
    $Cpte_AD_LastLogonTimeStamp = $member.LastLogonTimeStamp
    $Cpte_AD_LastLogonTimeStamp_Conv_Fr = [datetime]::FromFileTime($Cpte_AD_LastLogonTimeStamp).ToString('dd/MM/yyyy')
    $Cpte_AD_LastLogonTimeStamp_Conv = [datetime]::FromFileTime($Cpte_AD_LastLogonTimeStamp)
    If ($Cpte_AD_LastLogonTimeStamp_Conv_Fr -eq "01/01/1601") {$Cpte_AD_LastLogonTimeStamp_Conv_Fr = "Jamais"}
    $Cpte_AD_PasswordExpired = $member.PasswordExpired   
    $Cpte_AD_PasswordLastSet = $member.PasswordLastSet
    $Cpte_AD_PasswordNeverExpires = $member.PasswordNeverExpires
    $Cpte_AD_PasswordNotRequired = $member.PasswordNotRequired
    $Cpte_AD_whenCreated = $member.whenCreated
    $Cpte_AD_whenCreated_Conv_Fr = ($Cpte_AD_whenCreated).ToString('dd/MM/yyyy')

    $Val_Replace = "/" + $Cpte_AD_Name
    $OU = $Cpte_AD_CanonicalName.Replace($Val_Replace,"")
    
    If ($Cpte_AD_PasswordNeverExpires -eq $False) {
        $Nb = $Nb + 1
        get-aduser $Cpte_AD_Session -properties PasswordNeverExpires | set-aduser -PasswordNeverExpires $True  # Update to value True
        Add-Content -Path $Results_File -Value ($Cpte_AD_Session + ";" + $Cpte_AD_Name + ";" + $OU + ";" + $Cpte_AD_pwdLastSet_Conv_Fr + ";" + $Cpte_AD_lastLogon_Conv_Fr + ";" + $Cpte_AD_LastLogonTimeStamp_Conv_Fr + ";" + $Cpte_AD_Enabled)
    }

} # Foreach end


Invoke-Item $Path

